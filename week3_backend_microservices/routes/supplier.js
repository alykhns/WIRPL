// routes/supplier.js
const router = require('express').Router();
const { supplierDB } = require('../config/databases');

router.get('/', async (req, res) => {
  const [rows] = await supplierDB.query('SELECT * FROM suppliers WHERE is_active = TRUE');
  res.json(rows);
});

router.get('/:id/products', async (req, res) => {
  const [rows] = await supplierDB.query(
    'SELECT * FROM supplier_products WHERE supplier_id = ?', [req.params.id]
  );
  res.json(rows);
});

router.post('/purchase-order', async (req, res) => {
  const { supplier_id, items, expected_delivery } = req.body;
  const total = items.reduce((sum, i) => sum + i.quantity * i.unit_price, 0);
  const [po] = await supplierDB.query(
    'INSERT INTO purchase_orders (supplier_id, total_amount, expected_delivery) VALUES (?,?,?)',
    [supplier_id, total, expected_delivery]
  );
  for (const item of items) {
    await supplierDB.query(
      'INSERT INTO po_items (po_id, product_ref_id, quantity, unit_price) VALUES (?,?,?,?)',
      [po.insertId, item.product_ref_id, item.quantity, item.unit_price]
    );
  }
  res.status(201).json({ message: 'Purchase Order dibuat', po_id: po.insertId });
});

module.exports = router;
