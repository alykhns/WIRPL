// routes/logistics.js
const router = require('express').Router();
const { logisticsDB } = require('../config/databases');

router.get('/couriers', async (req, res) => {
  const [rows] = await logisticsDB.query('SELECT * FROM couriers WHERE is_active = TRUE');
  res.json(rows);
});

router.get('/track/:tracking_number', async (req, res) => {
  const [rows] = await logisticsDB.query(
    'SELECT s.*, c.courier_name FROM shipments s JOIN couriers c ON s.courier_id = c.courier_id WHERE s.tracking_number = ?',
    [req.params.tracking_number]
  );
  if (!rows.length) return res.status(404).json({ error: 'Tracking tidak ditemukan' });
  const [history] = await logisticsDB.query(
    'SELECT * FROM tracking_history WHERE shipment_id = ? ORDER BY recorded_at DESC',
    [rows[0].shipment_id]
  );
  res.json({ shipment: rows[0], history });
});

router.put('/shipments/:order_id/status', async (req, res) => {
  const { status, location, note } = req.body;
  const [shipment] = await logisticsDB.query(
    'SELECT shipment_id FROM shipments WHERE order_id = ?', [req.params.order_id]
  );
  if (!shipment.length) return res.status(404).json({ error: 'Shipment tidak ditemukan' });
  await logisticsDB.query(
    'UPDATE shipments SET shipping_status = ? WHERE order_id = ?',
    [status, req.params.order_id]
  );
  await logisticsDB.query(
    'INSERT INTO tracking_history (shipment_id, location, status_note) VALUES (?,?,?)',
    [shipment[0].shipment_id, location, note]
  );
  res.json({ message: 'Status pengiriman diupdate' });
});

module.exports = router;
