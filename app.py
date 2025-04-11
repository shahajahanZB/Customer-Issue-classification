from flask import Flask, jsonify, request, render_template, redirect, session, url_for
from model import Session, Message, initialize_db, Base, engine, Team, TeamMember
from functools import wraps

app = Flask(__name__)

# Add secret key for session
app.secret_key = 'your-secret-key-here'  # Change this in production

# Admin credentials (move to secure storage in production)
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin@example.com"

# Ensure database and tables exist
Base.metadata.create_all(engine)
initialize_db()

def get_nav_items(active_page):
    return [
        {'name': 'Overview', 'url': '/', 'active': active_page == 'overview'},
        {'name': 'Queries', 'url': '/queries', 'active': active_page == 'queries'},
        {'name': 'Teams', 'url': '/teams', 'active': active_page == 'teams'},
        {'name': 'Reports', 'url': '/reports', 'active': active_page == 'reports'},
        {'name': 'Settings', 'url': '/settings', 'active': active_page == 'settings'}
    ]

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['user_type'] = 'admin'
            return redirect(url_for('home'))
        
        # Check for team member
        db_session = Session()
        member = db_session.query(TeamMember).filter_by(email=email).first()
        
        if member and password == member.email:  # Using email as password
            session['user_type'] = 'member'
            session['member_id'] = member.id
            return redirect(url_for('member_dashboard'))
        
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Add login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_type' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def home():
    if session.get('user_type') != 'admin':
        return redirect(url_for('member_dashboard'))
    table_headers = ['Query Numbers', 'Message', 
                    'Routing Team', 'Confidentiality Level', 'Query Type','Query Status']
    
    return render_template('admin.html',
                         nav_items=get_nav_items('overview'),
                         table_headers=table_headers)

@app.route('/teams')
@login_required
def teams():
    db_session = Session()
    all_teams = db_session.query(Team).all()
    return render_template('team.html',
                         nav_items=get_nav_items('teams'),
                         teams=all_teams)

@app.route('/api/messages', methods=['GET'])
@login_required
def get_messages():
    session = Session()
    messages = session.query(Message).all()
    return jsonify([{
        '_id': message.id,
        'queryNumber': message.queryNumber,
        'message': message.message,
        'routingTeam': message.routingTeam,
        'queryType': message.queryType,  # Added queryType field
        'confidentialityLevel': message.confidentialityLevel,
        'status': message.status
    } for message in messages])

@app.route('/api/messages/<message_id>/solve', methods=['POST'])
@login_required
def solve_message(message_id):
    try:
        session = Session()
        message = session.query(Message).filter_by(id=message_id).first()
        if message:
            message.status = 'Solved'
            session.commit()
            return jsonify({'message': 'Message marked as solved!'})
        return jsonify({'error': 'Message not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/team')
@login_required
def team_management():
    return render_template('team.html', nav_items=get_nav_items('teams'))

@app.route('/api/teams', methods=['GET'])
@login_required
def get_teams():
    try:
        session = Session()
        teams = session.query(Team).all()
        return jsonify([{
            'id': team.id,
            'name': team.name,
            'category': team.category or team.name,  # Fallback to name if category is None
            'members': [{
                'id': member.id,
                'name': member.name,
                'email': member.email,
                'role': member.role,
                'status': member.status,
                'issues_solved': member.issues_solved
            } for member in team.members]
        } for team in teams])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@app.route('/api/teams/<int:team_id>', methods=['GET'])
def get_team_details(team_id):
    try:
        db_session = Session()
        team = db_session.query(Team).get(team_id)
        if not team:
            return jsonify({'error': 'Team not found'}), 404
            
        return jsonify({
            'id': team.id,
            'name': team.name,
            'members': [{
                'id': member.id,
                'name': member.name,
                'email': member.email,
                'role': member.role,
                'status': member.status,
                'issues_solved': member.issues_solved
            } for member in team.members]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db_session.close()

@app.route('/api/teams/<int:team_id>/members', methods=['POST'])
@login_required  # Add login requirement
def add_team_member(team_id):
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        print(f"Adding member to team {team_id}. Data:", data)  # Debug log
        
        required_fields = ['name', 'email', 'role']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        db_session = Session()
        team = db_session.query(Team).get(team_id)
        
        if not team:
            return jsonify({'error': f'Team with id {team_id} not found'}), 404
            
        # Check if email already exists
        existing_member = db_session.query(TeamMember).filter_by(email=data['email']).first()
        if existing_member:
            return jsonify({'error': 'Email already registered'}), 409
            
        member = TeamMember(
            name=data['name'],
            email=data['email'],
            role=data['role'],
            team_id=team_id,
            status='active',
            issues_solved=0
        )
        
        db_session.add(member)
        db_session.commit()
        
        print(f"Successfully added member {member.id} to team {team_id}")  # Debug log
        
        return jsonify({
            'message': 'Member added successfully',
            'member': {
                'id': member.id,
                'name': member.name,
                'email': member.email,
                'role': member.role,
                'status': member.status,
                'issues_solved': member.issues_solved
            }
        })
        
    except Exception as e:
        print(f"Error adding member to team {team_id}:", str(e))  # Debug log
        db_session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db_session.close()

@app.route('/member/dashboard')
@login_required
def member_dashboard():
    if session.get('user_type') != 'member':
        return redirect(url_for('home'))
    # Get member from session
    member_id = session.get('member_id')
    if not member_id:
        return redirect('/login')
    
    db_session = Session()
    member = db_session.query(TeamMember).get(member_id)
    return render_template('member_dashboard.html', 
                         member=member,
                         nav_items=get_nav_items('dashboard'))

@app.route('/api/member/queries')
@login_required
def get_member_queries():
    member_id = session.get('member_id')
    if not member_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    db_session = Session()
    member = db_session.query(TeamMember).get(member_id)
    team_queries = db_session.query(Message).filter_by(routingTeam=member.team.name).all()
    
    return jsonify([{
        'id': q.id,
        'queryNumber': q.queryNumber,
        'message': q.message,
        'queryType': q.queryType,
        'status': q.status
    } for q in team_queries])

@app.route('/api/member/queries/<int:query_id>/solve', methods=['POST'])
@login_required
def solve_query(query_id):
    member_id = session.get('member_id')
    if not member_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    db_session = Session()
    query = db_session.query(Message).get(query_id)
    member = db_session.query(TeamMember).get(member_id)
    
    query.status = 'Solved'
    member.issues_solved += 1
    db_session.commit()
    
    return jsonify({'message': 'Query marked as solved'})

if __name__ == '__main__':
    app.run(debug=True)