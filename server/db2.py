import pymysql
import json

cnx = pymysql.connect(user='scam_protector', password='scamprotect', host='scamprotect.c9hhucpxn2q2.us-east-1.rds.amazonaws.com', database='scam_protect')
cursor = cnx.cursor()


email = "thisisatest@gmail.com"
##print("SELECT ID FROM user_email WHERE EMAIL='{0}'".format(email))
query = ("INSERT INTO user_token (USER_ID, TOKEN, vtu_email) values ({0}, '{1}', '{2}')".format("1", "this worked","please"))
cursor.execute(query)
cnx.commit()

