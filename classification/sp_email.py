'''
email.py

Representation of an email object.

label = integer (0 or 1) --> 0 meaning "probably not a scam attempt" and 
1 meaning "definitely a scam attempt."
'''
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import Column, Integer, String

Base = declarative_base() # NOTE: It may be super hacky to do things this way, but this is how I did it.

class ScamProtectorEmail(Base):
	__tablename__ = 'email'

	id = Column(Integer, primary_key=True)
	full_text = Column(LONGTEXT, nullable=True)
	label = Column(Integer, nullable=True)

	def __init__(self, full_text, label):
		self.full_text = full_text
		self.label = label
		self.feature_vals = {}

		# load features, etc.