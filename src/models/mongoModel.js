// models/mongoModel.js
const MongoClient = require('mongodb').MongoClient;

const mongo_url = 'mongodb://magangitg:bWFnYW5naXRn@database2.pptik.id:27017/magangitg';
const mongo_db = 'magangitg';
const mongo_collection_name = 'ktp_ocr';

let mongo_collection;

async function createMongoConnection() {
  const client = await MongoClient.connect(mongo_url, { useNewUrlParser: true, useUnifiedTopology: true });
  const db = client.db(mongo_db);
  mongo_collection = db.collection(mongo_collection_name);
  console.log('MongoDB connection and collection initialized successfully.');
}

createMongoConnection();

module.exports = { mongo_collection, createMongoConnection };
