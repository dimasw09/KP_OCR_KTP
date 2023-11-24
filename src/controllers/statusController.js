// controllers/statusController.js
const { mongo_collection } = require('../models/mongoModel');

async function checkStatus(req, res) {
  try {
    const filename = req.params.filename;
    const result = await mongo_collection.findOne({ name_file: filename }); // changed to name_file

    if (result) {
      const receipt = result.receipt || 'unknown';
      const status = result.status || 'unknown';
      res.json({ receipt, status, filename });
    } else {
      res.json({ error: 'File not found in the database.' });
    }
  } catch (error) {
    res.json({ error: `An error occurred: ${error.message || 'unknown'}` });
  }
}

module.exports = { checkStatus };
