'''
email.py

Representation of an email object.

label = integer (0 or 1) --> 0 meaning "probably not a scam attempt" and 
1 meaning "definitely a scam attempt."
'''
class Email():

	def __init__(self, text, label):
		self.text = text
		self.label = label
		self.feature_vals = {}

		# load features, etc.