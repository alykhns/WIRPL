// routes/orders.js — MICROSERVICE UTAMA
// Checkout: orchestrate mainDB + paymentDB + logisticsDB sekaligus
const router = require('express').Router();
const { mainDB, paymentDB, logisticsDB } = require('../config/databases');

// GET /api/orders — Semua orders
router.get('/', async (req, res) => {
  try {
    const [orders] = await mainDB.query(
      'SELECT * FROM orders ORDER BY created_at DESC'
    );
    res.json(orders);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /api/orders/:id — Detail order + payment + shipment (lintas DB)
router.get('/:id', async (req, res) => {
  try {
    const [order] = await mainDB.query(
      'SELECT o.*, u.username FROM orders o JOIN users u ON o.buyer_id = u.user_id WHERE o.order_id = ?',
      [req.params.id]
    );
    if (!order.length) return res.status(404).json({ error: 'Order tidak ditemukan' });

    // Ambil payment dari lumiere_payment
    const [payment] = await paymentDB.query(
      'SELECT * FROM payment_transactions WHERE order_id = ?', [req.params.id]
    );

    // Ambil shipment dari lumiere_logistics
    const [shipment] = await logisticsDB.query(
      'SELECT s.*, c.courier_name, c.service_type FROM shipments s JOIN couriers c ON s.courier_id = c.courier_id WHERE s.order_id = ?',
      [req.params.id]
    );

    res.json({
      order: order[0],
      payment: payment[0] || null,
      shipment: shipment[0] || null,
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// POST /api/orders/checkout — Checkout (orchestrate 3 database)
router.post('/checkout', async (req, res) => {
  const { buyer_id, institution_id, total_amount, items, payment_method_id, courier_id } = req.body;
  try {
    // 1. Buat order di mainDB
    const [orderResult] = await mainDB.query(
      'INSERT INTO orders (buyer_id, institution_id, total_amount, order_status) VALUES (?,?,?,?)',
      [buyer_id, institution_id, total_amount, 'order']
    );
    const order_id = orderResult.insertId;

    // 2. Insert order items dan kurangi stok
    for (const item of items) {
      await mainDB.query(
        'INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES (?,?,?,?)',
        [order_id, item.product_id, item.quantity, item.price]
      );
      await mainDB.query(
        'UPDATE products SET stock = stock - ? WHERE product_id = ?',
        [item.quantity, item.product_id]
      );
    }

    // 3. Buat payment transaction di lumiere_payment
    await paymentDB.query(
      'INSERT INTO payment_transactions (order_id, method_id, amount, status) VALUES (?,?,?,?)',
      [order_id, payment_method_id, total_amount, 'pending']
    );

    // 4. Buat shipment di lumiere_logistics
    const tracking = 'LMR-' + Date.now();
    await logisticsDB.query(
      'INSERT INTO shipments (order_id, courier_id, tracking_number, shipping_status) VALUES (?,?,?,?)',
      [order_id, courier_id, tracking, 'preparing']
    );

    res.status(201).json({
      message: 'Checkout berhasil!',
      order_id,
      tracking_number: tracking,
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
