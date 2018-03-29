'''
email.py

Representation of an email object.

label = integer (0 or 1)
'''
class Email():

	def __init__(text, label):
		self.text = text
		self.label = label
		self.feature_vals = {}

		# load features, etc.