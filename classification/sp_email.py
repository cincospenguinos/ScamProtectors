'''
email.py

Representation of an email object.

label = integer (0 or 1) --> 0 meaning "probably not a scam attempt" and 
1 meaning "definitely a scam attempt."
'''
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class ScamProtectorEmail(Base):
	__tablename__ = 'email'

	id = Column(Integer, primary_key=True)
	text = Column(String, nullable=True)
	label = Column(Integer, nullable=True)

	def __init__(self, text, label):
		self.text = text
		self.label = label
		self.feature_vals = {}

		# load features, etc.