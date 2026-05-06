// routes/auth.js — Auth dari lumiere_tenant_1
const router = require('express').Router();
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { mainDB } = require('../config/databases');

// POST /api/auth/register
router.post('/register', async (req, res) => {
  try {
    const { username, email, password, first_name, last_name } = req.body;
    const hashed = await bcrypt.hash(password, 10);
    const [result] = await mainDB.query(
      'INSERT INTO users (username, email, password_hash, first_name, last_name) VALUES (?,?,?,?,?)',
      [username, email, hashed, first_name, last_name]
    );
    res.status(201).json({ message: 'Registrasi berhasil', user_id: result.insertId });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// POST /api/auth/login
router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    const [rows] = await mainDB.query('SELECT * FROM users WHERE email = ?', [email]);
    if (!rows.length) return res.status(401).json({ error: 'Email tidak ditemukan' });

    const user = rows[0];
    const valid = await bcrypt.compare(password, user.password_hash);
    if (!valid) return res.status(401).json({ error: 'Password salah' });

    const token = jwt.sign(
      { user_id: user.user_id, email: user.email },
      process.env.JWT_SECRET,
      { expiresIn: '24h' }
    );
    res.json({ token, user: { user_id: user.user_id, username: user.username, email: user.email } });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
