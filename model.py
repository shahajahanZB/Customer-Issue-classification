from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, joinedload

Base = declarative_base()
engine = create_engine('sqlite:///dashboard.db', echo=False)  # Set echo=False to reduce logs
Session = sessionmaker(bind=engine)

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    queryNumber = Column(Integer, unique=True)
    message = Column(String)
    routingTeam = Column(String)
    queryType = Column(String)  # Added queryType field
    confidentialityLevel = Column(Integer)  # 0-100 percentage
    status = Column(String, default='Pending')
    assigned_to = Column(Integer, ForeignKey('team_members.id'), nullable=True)
    assigned_member = relationship('TeamMember', backref='assigned_tasks')

class Team(Base):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    category = Column(String)
    members = relationship('TeamMember', back_populates='team', lazy='joined')

class TeamMember(Base):
    __tablename__ = 'team_members'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    role = Column(String)
    status = Column(String, default='active')
    team_id = Column(Integer, ForeignKey('teams.id'))
    issues_solved = Column(Integer, default=0)
    team = relationship('Team', back_populates='members', lazy='joined')

class PasswordReset(Base):
    __tablename__ = 'password_resets'
    
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('team_members.id'))
    requested_at = Column(String)
    status = Column(String, default='pending')  # pending, approved, rejected
    member = relationship('TeamMember', backref='password_resets')

def initialize_teams():
    session = Session()
    try:
        teams = [
            Team(name='Technical Support', category='Support'),
            Team(name='Billing Support', category='Support'),
            Team(name='Account Support', category='Support'),
            Team(name='Product Support', category='Support'),
            Team(name='Feature Request', category='Development'),
            Team(name='Bug Report', category='Development'),
            Team(name='General Inquiry', category='Customer Service'),
            Team(name='Other', category='Miscellaneous'),
            Team(name='Customer Service', category='Support'),
            Team(name='Sales Support', category='Sales')
        ]
        session.add_all(teams)
        session.commit()
        print("Teams initialized successfully")
    except Exception as e:
        print(f"Error initializing teams: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()

def initialize_db():
    # Create all tables if they don't exist
    Base.metadata.create_all(engine)
    
    session = Session()
    try:
        # Initialize teams only if teams table is empty
        if session.query(Team).count() == 0:
            initialize_teams()
            
            # Add sample messages only if messages table is empty
            if session.query(Message).count() == 0:
                sample_messages = [
                    Message(
                        queryNumber=1,
                        message="System outage in region A",
                        routingTeam="Technical Support",
                        queryType="Technical Support",
                        confidentialityLevel=90,
                        status="Pending"
                    ),
                    Message(
                        queryNumber=2,
                        message="Request for new hardware",
                        routingTeam="Product Support",
                        queryType="Product Support",
                        confidentialityLevel=50,
                        status="Pending"
                    )
                ]
                session.add_all(sample_messages)
                session.commit()
                print("Database initialized with sample data.")
            else:
                print("Messages table already contains data.")
        else:
            print("Teams table already contains data.")
    except Exception as e:
        print(f"Error during database initialization: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    initialize_db()
