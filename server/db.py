import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
from sqlalchemy.orm import sessionmaker

builtin_list = list


db = SQLAlchemy()


def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)


def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data





engine = create_engine('postgresql://usr:pass@localhost:5432/sqlalchemy')
Session = sessionmaker(bind=engine)

Base = declarative_base()

Base = declarative_base()
 

CLOUDSQL_CONNECTION_NAME = "scam-protect:us-central1:scam-protect"
CLOUDSQL_USER = "Jess"
CLOUDSQL_PASSWORD = "scamprotect"

class User(Base):
    __tablename__ = 'USER_EMAIL'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    ID = Column(Integer, primary_key=True)
    EMAIL = Column(String(50), nullable=False)

    def __repr__(self):
        return "<User(ID='%i', EMAIL=%s)" % (self.ID, self.EMAIL)

    def __init__(self, email):
        self.EMAIL = email

class Token(Base):
    __tablename__ = 'TOKENS'
    TOKEN_ID = Column(Integer, primary_key=True)
    USER_ID = Column(Integer, ForeignKey('USER_EMAIL.ID'))
    TOKEN = Column(String(100), nullable=False)
    
    def __init__(self, user_id, token):
        self.USER_ID = user_id
        self.TOKEN = token