// server.js — Lumiere API Gateway (Microservice Layer)
// Ini adalah "bintang" di tengah diagram — menghubungkan semua database
require('dotenv').config();
const express = require('express');
const cors = require('cors');
const { testAllConnections } = require('./config/databases');

const app = express();
app.use(cors());
app.use(express.json());

// ── Routes (tiap service punya route sendiri) ──
app.use('/api/auth',      require('./routes/auth'));
app.use('/api/products',  require('./routes/products'));
app.use('/api/orders',    require('./routes/orders'));
app.use('/api/payment',   require('./routes/payment'));
app.use('/api/logistics', require('./routes/logistics'));
app.use('/api/supplier',  require('./routes/supplier'));

// Health check — cek semua DB terhubung
app.get('/health', async (req, res) => {
  res.json({ status: 'Lumiere API Gateway running', timestamp: new Date() });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, async () => {
  console.log(`\n🚀 Lumiere API Gateway running on http://localhost:${PORT}`);
  console.log('📦 Testing all database connections...\n');
  await testAllConnections();
});
