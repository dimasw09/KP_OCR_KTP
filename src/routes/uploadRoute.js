// routes/uploadRoute.js
const express = require('express');
const { handleFileUpload } = require('../controllers/uploadController');
const multer = require('multer');

// Create and configure multer middleware
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

const router = express.Router();

router.post('/', upload.single('image'), handleFileUpload);

module.exports = router;
