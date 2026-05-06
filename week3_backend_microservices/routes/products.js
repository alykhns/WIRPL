// routes/products.js — Products dari lumiere_tenant_1
const router = require('express').Router();
const { mainDB } = require('../config/databases');

// GET /api/products — Semua produk
router.get('/', async (req, res) => {
  try {
    const [rows] = await mainDB.query(
      'SELECT * FROM products ORDER BY created_at DESC'
    );
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /api/products/:id — Detail produk
router.get('/:id', async (req, res) => {
  try {
    const [rows] = await mainDB.query(
      'SELECT * FROM products WHERE product_id = ?', [req.params.id]
    );
    if (!rows.length) return res.status(404).json({ error: 'Produk tidak ditemukan' });
    res.json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// POST /api/products — Tambah produk
router.post('/', async (req, res) => {
  try {
    const { product_name, description, price, stock } = req.body;
    const [result] = await mainDB.query(
      'INSERT INTO products (product_name, description, price, stock) VALUES (?,?,?,?)',
      [product_name, description, price, stock]
    );
    res.status(201).json({ product_id: result.insertId, message: 'Produk ditambahkan' });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// PUT /api/products/:id — Update produk
router.put('/:id', async (req, res) => {
  try {
    const { product_name, description, price, stock } = req.body;
    await mainDB.query(
      'UPDATE products SET product_name=?, description=?, price=?, stock=? WHERE product_id=?',
      [product_name, description, price, stock, req.params.id]
    );
    res.json({ message: 'Produk diupdate' });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// DELETE /api/products/:id — Hapus produk
router.delete('/:id', async (req, res) => {
  try {
    await mainDB.query('DELETE FROM products WHERE product_id = ?', [req.params.id]);
    res.json({ message: 'Produk dihapus' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
