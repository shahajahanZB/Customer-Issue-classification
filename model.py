from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, joinedload

Base = declarative_base()
engine = create_engine('sqlite:///dashboard.db', echo=False)  # Set echo=False to reduce logs
Session = sessionmaker(bind=engine)

QUERY_TYPES = [
    "Booking Issue",
    "Subscription Plan Issue",
    "Payment Issue",
    "Driver No Show Issue",
    "Ride Delay Issue",
    "Route Issue",
    "Account Profile Issue",
    "Customer Support Issue",
    "Junk Message",
]

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

    @staticmethod
    def get_valid_teams():
        session = Session()
        try:
            return [team.name for team in session.query(Team).all()]
        finally:
            session.close()
            
    def __init__(self, **kwargs):
        if 'routingTeam' in kwargs:
            valid_teams = self.get_valid_teams()
            if kwargs['routingTeam'] not in valid_teams:
                kwargs['routingTeam'] = 'Other'
        super().__init__(**kwargs)

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
    password = Column(String)  # Will be set to email by default
    role = Column(String)
    status = Column(String, default='inactive')  # Changed default to inactive
    team_id = Column(Integer, ForeignKey('teams.id'))
    issues_solved = Column(Integer, default=0)
    team = relationship('Team', back_populates='members', lazy='joined')
    
    def __init__(self, **kwargs):
        if 'status' not in kwargs:
            kwargs['status'] = 'inactive'  # Ensure new members start as inactive
        super().__init__(**kwargs)
        # Set default password as email if not provided
        if not self.password and self.email:
            self.password = self.email

    def update_status(self, new_status):
        self.status = new_status
        
    @property
    def is_active(self):
        return self.status == 'active'

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
            Team(name='Bookings', category='Booking Issue'),
            Team(name='Subscriptions', category='Subscription Plan Issue'),
            Team(name='Payments', category='Payment Issue'),
            Team(name='Driver Operations', category='Driver No Show Issue'),
            Team(name='Ride Operations', category='Ride Delay Issue'),
            Team(name='Route Operations', category='Route Issue'),
            Team(name='Account Management', category='Account Profile Issue'),
            Team(name='Support', category='Customer Support Issue'),
            Team(name='Admin', category='Junk Message')
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
                        message="Unable to book a ride for tomorrow",
                        routingTeam="Bookings",  # Updated to match team name
                        queryType="Booking Issue",
                        confidentialityLevel=80,
                        status="Pending"
                    ),
                    Message(
                        queryNumber=2,
                        message="Driver didn't show up for pickup",
                        routingTeam="Driver Operations",  # Updated to match team name
                        queryType="Driver No Show Issue",
                        confidentialityLevel=90,
                        status="Pending"
                    ),
                    Message(
                        queryNumber=3,
                        message="Subscription renewal failed",
                        routingTeam="Subscriptions",  # Updated to match team name
                        queryType="Subscription Plan Issue",
                        confidentialityLevel=70,
                        status="Pending"
                    ),
                    Message(
                        queryNumber=4,
                        message="Driver took wrong route",
                        routingTeam="Route Operations",  # Updated to match team name
                        queryType="Route Issue",
                        confidentialityLevel=60,
                        status="Pending"
                    ),
                    Message(
                        queryNumber=5,
                        message="Payment failed multiple times",
                        routingTeam="Payments",  # Updated to match team name
                        queryType="Payment Issue",
                        confidentialityLevel=85,
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
