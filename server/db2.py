import mysql.connector
import json

cnx = mysql.connector.connect(user='scam_protector', password='scamprotect', host='scamprotect.c9hhucpxn2q2.us-east-1.rds.amazonaws.com', database='scam_protect')
cursor = cnx.cursor()


email = "thisisatest@gmail.com"
print("SELECT ID FROM user_email WHERE EMAIL='{0}'".format(email))
query = ("SELECT ID FROM user_email WHERE EMAIL='{0}'".format(email))
cursor.execute(query)

for token in cursor:
    print(token)