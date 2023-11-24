// controllers/uploadController.js
const fs = require('fs');
const ftp = require('basic-ftp');
const path = require('path'); 
const { sendToQueue } = require('./rabbitmqController');
const { uploadToFTP } = require('./ftpController');
const { createMongoConnection } = require('../models/mongoModel');
const uuid = require('uuid');

// Call createMongoConnection to initialize mongo_collection
createMongoConnection();

async function handleFileUpload(req, res) {
  try {
    const image_file = req.file;
    if (image_file) {
      const file_uuid = uuid.v4();
      const new_filename = `${file_uuid}.png`;

      const receipt = new_filename;

      const temp_path = `uploads/${new_filename}`;
      fs.writeFileSync(temp_path, image_file.buffer);

      await uploadToFTP(temp_path, new_filename);
      await sendToQueue(new_filename, receipt); // changed to new_filename
      const no_ext = path.parse(new_filename).name;

      res.json({
        receipt: no_ext,
        message: 'File uploaded successfully.',
      });
    } else {
      const error_message = 'No image uploaded.';
      res.json({ error: error_message });
    }
  } catch (error) {
    const error_message = error.message || 'An error occurred.';
    res.json({ error: error_message });
  }
}

module.exports = { handleFileUpload };
