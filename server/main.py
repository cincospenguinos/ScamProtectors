# /server.py

import json,os
from six.moves.urllib.request import urlopen
from functools import wraps

from flask import Flask, request, jsonify, _request_ctx_stack
from flask_cors import cross_origin
from jose import jwt
import pymysql

vtus = [
  { "email": "testing@gmail.com" },
  { "email": "testing2@gmail.com" },
  { "email": "jesslarsen21@gmail.com" }
]
cnx = pymysql.connect(user='scam_protector', password='scamprotect', host='scamprotect.c9hhucpxn2q2.us-east-1.rds.amazonaws.com', database='scam_protect')
cursor = cnx.cursor()

AUTH0_DOMAIN = 'scam-protector.auth0.com'
API_AUDIENCE = "http://google_api"
ALGORITHMS = ["RS256"]

app = Flask(__name__)

# Format error response and append status code
def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)
    
    parts = auth.split()
    
    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token

def requires_auth(f):
    """Determines if the Access Token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                "description":
                                    "incorrect claims,"
                                    "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                "description":
                                    "Unable to parse authentication"
                                    " token."}, 401)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                        "description": "Unable to find appropriate key"}, 401)
    return decorated

# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
    
@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


# Controllers API

# This doesn't need authentication
@app.route("/api/public")
@cross_origin(headers=['Content-Type', 'Authorization'])
def public():
    return "hello world"

# This does need authentication
@app.route("/api/authenticated-emails/<email>")
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def get_authenticated_emails(email):
    query = ("SELECT ID FROM user_email WHERE EMAIL='{0}'".format(email))
    cursor.execute(query)
    email_id = cursor.fetchone()[0]
    print(email_id)
    query = ("SELECT TOKEN FROM user_token WHERE USER_ID={0}".format(email_id))

    cursor.execute(query)
    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    rv = cursor.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)

@app.route("/api/vtus")
@cross_origin(headers=['Content-Type', 'Authorization'])
def get_vtus():
    return jsonify(vtus)

if __name__ == '__main__':
    app.run(port=8083)
