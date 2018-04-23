/*
 |--------------------------------------
 | Vtu Model
 |--------------------------------------
 */

const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const vtuSchema = new Schema({
  email: { type: String, required: true },
  caretaker: { type: String, required: true },
  token: { type: String, required: true }
});

module.exports = mongoose.model('Vtu', vtuSchema);