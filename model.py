from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
engine = create_engine('sqlite:///dashboard.db', echo=True)
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

class Team(Base):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    category = Column(String)
    members = relationship('TeamMember', backref='team')

class TeamMember(Base):
    __tablename__ = 'team_members'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    role = Column(String)
    status = Column(String, default='active')
    team_id = Column(Integer, ForeignKey('teams.id'))
    issues_solved = Column(Integer, default=0)

def initialize_teams():
    session = Session()
    if session.query(Team).count() == 0:
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
        try:
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

def initialize_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    initialize_teams()
    session = Session()
    
    # Add sample data if table is empty
    if session.query(Message).count() == 0:
        sample_messages = [
            Message(
                queryNumber=1,
                message="System outage in region A",
                routingTeam="Technical Support",
                queryType="Technical Support",
                confidentialityLevel=90,  # High confidentiality
                status="Pending"
            ),
            Message(
                queryNumber=2,
                message="Request for new hardware",
                routingTeam="Product Support",
                queryType="Product Support",
                confidentialityLevel=50,  # Medium confidentiality
                status="Pending"
            )
        ]
        session.add_all(sample_messages)
        session.commit()
        print("Database initialized with sample data.")
    else:
        print("Database already initialized.")

if __name__ == "__main__":
    initialize_db()
