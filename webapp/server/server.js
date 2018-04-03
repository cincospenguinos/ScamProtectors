const express = require('express')
const app = express()

app.get('/', function (req, res) {
  res.send('Hello World!')
})
app.get('/help', function (req, res) {
  res.send('You did it!')
})
app.listen(3000, function () {
  console.log('Example app listening on port 3000!')
})