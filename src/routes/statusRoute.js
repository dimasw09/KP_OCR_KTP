// routes/statusRoute.js
const express = require('express');
const { checkStatus } = require('../controllers/statusController');

const router = express.Router();

router.get('/check_status/:filename', checkStatus);

module.exports = router;
