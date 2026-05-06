// routes/payment.js
const router = require('express').Router();
const { paymentDB } = require('../config/databases');

// GET /api/payment/methods
router.get('/methods', async (req, res) => {
  const [rows] = await paymentDB.query('SELECT * FROM payment_methods WHERE is_active = TRUE');
  res.json(rows);
});

// GET /api/payment/:order_id
router.get('/:order_id', async (req, res) => {
  const [rows] = await paymentDB.query(
    'SELECT pt.*, pm.method_name, pm.provider FROM payment_transactions pt JOIN payment_methods pm ON pt.method_id = pm.method_id WHERE pt.order_id = ?',
    [req.params.order_id]
  );
  res.json(rows[0] || null);
});

// PUT /api/payment/:transaction_id/confirm — Konfirmasi pembayaran
router.put('/:transaction_id/confirm', async (req, res) => {
  await paymentDB.query(
    'UPDATE payment_transactions SET status="success", paid_at=NOW() WHERE transaction_id=?',
    [req.params.transaction_id]
  );
  res.json({ message: 'Pembayaran dikonfirmasi' });
});

module.exports = router;
