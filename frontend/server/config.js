// server/config.js
module.exports = {
    AUTH0_DOMAIN: 'scam-protector.auth0.com', // e.g., kmaida.auth0.com
    AUTH0_API_AUDIENCE: 'http://localhost:4200/', // e.g., 'http://localhost:8083/api/'
    MONGO_URI: process.env.MONGO_URI || 'mongodb://scamprotector1:scamprotectorusr1@ds251598.mlab.com:51598/scamprotector', //'mongodb://[USER]:[PASSWORD]@[DS######].mlab.com:[PORT]/[DB_NAME]'
    NAMESPACE: 'http://myapp.com/roles'
};