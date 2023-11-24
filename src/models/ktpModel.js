// ktpModel.js
const mongoose = require("mongoose");
const Schema = mongoose.Schema;
const moment = require("moment");

const ktpSchema = new Schema({
  name_file: { 
    type: String,
    required: true,
  },
  receipt: {
    type: String,
    required: true,
  },
  NIK: {
    type: Number,
    required: true,
  },
  Nama: {
    type: String,
    required: false,
  },
  createAt: {
    type: String,
    default: () => moment().format(),
  },
  updateAt: {
    type: String,
    default: () => moment().format(),
  },
  status: {
    type: String,
    required: true,
  },
});

const ktpModel = mongoose.model("KtpModel", ktpSchema);

module.exports = ktpModel;
