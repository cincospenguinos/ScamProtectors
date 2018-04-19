// server/api.js
/*
 |--------------------------------------
 | Dependencies
 |--------------------------------------
 */

const jwt = require('express-jwt');
const jwks = require('jwks-rsa');
const Event = require('./models/Event');
const Rsvp = require('./models/Rsvp');
const Vtu = require('./models/Vtu');

/*
 |--------------------------------------
 | Authentication Middleware
 |--------------------------------------
 */

module.exports = function(app, config) {
    // Authentication middleware
    const jwtCheck = jwt({
      secret: jwks.expressJwtSecret({
        cache: true,
        rateLimit: true,
        jwksRequestsPerMinute: 5,
        jwksUri: `https://${config.AUTH0_DOMAIN}/.well-known/jwks.json`
      }),
      audience: config.AUTH0_API_AUDIENCE,
      issuer: `https://${config.AUTH0_DOMAIN}/`,
      algorithm: 'RS256'
    });

    // Check for an authenticated admin user
  const adminCheck = (req, res, next) => {
    const roles = req.user[config.NAMESPACE] || [];
    if (roles.indexOf('admin') > -1) {
      next();
    } else {
      res.status(401).send({message: 'Not authorized for admin access'});
    }
  }

/*
 |--------------------------------------
 | API Routes
 |--------------------------------------
 */

  // GET API root
  // app.get('/api/', (req, res) => {
  //   res.send('API works');
  // });

  const _vtuListProjection = 'title';

  // GET list of public events starting in the future
  app.get('/api/vtus', (req, res) => {
    Vtu.find(_vtuListProjection, (err, vtus) => {
      let vtusArr = [];
      if (err) {
        return res.status(500).send({message: err.message});
      }
      if (vtus) {
        vtus.forEach(vtu => {
          vtusArr.push(vtu);
        });
      }
      res.send(vtusArr);
    });
  });

};