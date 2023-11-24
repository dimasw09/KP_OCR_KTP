// controllers/ftpController.js
const fs = require('fs');
const ftp = require('basic-ftp');

const FTP_SERVER = 'ftp5.pptik.id';
const FTP_PORT = 2121;
const FTP_USERNAME = 'magangitg';
const FTP_PASSWORD = 'bWFnYW5naXRn';
const FTP_UPLOAD_DIR = '/ktp_ocr';

async function uploadToFTP(file_path, filename) {
  const client = new ftp.Client();
  try {
    await client.access({
      host: FTP_SERVER,
      port: FTP_PORT,
      user: FTP_USERNAME,
      password: FTP_PASSWORD,
    });

    console.log(`Uploading ${filename} to FTP server.`);
    await client.uploadFrom(fs.createReadStream(file_path), `${FTP_UPLOAD_DIR}/${filename}`);
    console.log(`Upload completed for ${filename}.`);
  } catch (error) {
    console.error(`FTP upload failed: ${error.message}`);
  } finally {
    client.close();
  }
}

module.exports = { uploadToFTP };
