// config/databases.js
require('dotenv').config();
const mysql = require('mysql2/promise');

const sharedConfig = {
  user: process.env.DB_MAIN_USER,
  password: process.env.DB_MAIN_PASSWORD || '',
  socketPath: process.env.DB_SOCKET, // pakai socket XAMPP Mac
  waitForConnections: true,
  connectionLimit: 10,
};

const mainDB = mysql.createPool({
  ...sharedConfig,
  database: process.env.DB_MAIN_NAME,
});

const paymentDB = mysql.createPool({
  ...sharedConfig,
  database: process.env.DB_PAYMENT_NAME,
});

const logisticsDB = mysql.createPool({
  ...sharedConfig,
  database: process.env.DB_LOGISTICS_NAME,
});

const supplierDB = mysql.createPool({
  ...sharedConfig,
  database: process.env.DB_SUPPLIER_NAME,
});

async function testAllConnections() {
  const dbs = [
    { name: 'lumiere_tenant_1 (Main)', pool: mainDB },
    { name: 'lumiere_payment',         pool: paymentDB },
    { name: 'lumiere_logistics',       pool: logisticsDB },
    { name: 'lumiere_supplier',        pool: supplierDB },
  ];
  for (const db of dbs) {
    try {
      await db.pool.query('SELECT 1');
      console.log(`✅ Connected: ${db.name}`);
    } catch (err) {
      console.error(`❌ Failed: ${db.name} — ${err.message}`);
    }
  }
}

module.exports = { mainDB, paymentDB, logisticsDB, supplierDB, testAllConnections };
