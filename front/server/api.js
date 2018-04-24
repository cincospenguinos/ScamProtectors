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

module.exports = function (app, config) {
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
      res.status(401).send({ message: 'Not authorized for admin access' });
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

  // const _vtuListProjection = 'title';
  // const _vtuFlaggedListProjection = 'title';

  // GET list of VTUs under user
  app.get('/api/vtus', (req, res) => {
    let vtusArr = [];
    if (err) {
      return res.status(500).send({ message: err.message });
    }
    if (vtus) {
      vtus.forEach(vtu => {
        vtusArr.push(vtu);
      });
    }
    res.send(vtusArr);
  });

  // POST VTU under user
  app.post('/api/vtus', jwtCheck, (req, res) => {
    if (err) {
      return res.status(500).send({ message: err.message });
    }
    const vtu = new Vtu({
      email: req.body.email,
      token: req.body.token
    });
    vtu.save((err) => {
      if (err) {
        return res.status(500).send({ message: err.message });
      }
      res.send(vtu);
    });
  });


  // POST user to database
  app.post('/api/log-in', jwtCheck, (req, res) => {
    if (err) {
      return res.status(500).send({ message: err.message });
    }
    const vtu = new Vtu({
      email: req.body.email
    });
    vtu.save((err) => {
      if (err) {
        return res.status(500).send({ message: err.message });
      }
      res.send(vtu);
    });
  });

  // GET flagged emails under user's account
  app.get('/api/flagged-emails', (req, res) => {
    let flaggedVtusArr = [];
    if (err) {
      return res.status(500).send({ message: err.message });
    }
    if (vtus) {
      vtus.forEach(vtu => {
        flaggedVtusArr.push(vtu);
      });
    }
    res.send(flaggedVtusArr);
  });
};