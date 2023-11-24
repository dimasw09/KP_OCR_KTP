// controllers/rabbitmqController.js
const amqp = require('amqplib');

// RabbitMQ configurations
const RABBITMQ_HOST = 'localhost';
const RABBITMQ_QUEUE = 'image_queue';

async function sendToQueue(filename, receipt) {
  const connection = await amqp.connect(`amqp://${RABBITMQ_HOST}`);
  const channel = await connection.createChannel();

  try {
    await channel.assertQueue(RABBITMQ_QUEUE, { durable: false });
  } catch (error) {
    if (error.code !== 406) {
      throw error;
    }
  }

  channel.sendToQueue(RABBITMQ_QUEUE, Buffer.from(filename), {
    appId: receipt,
  });

  await channel.close();
  await connection.close();
}

module.exports = { sendToQueue };
