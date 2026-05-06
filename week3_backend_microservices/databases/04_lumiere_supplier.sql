-- ==========================================
-- LUMIERE SUPPLIER SERVICE DATABASE
-- Equivalent to: SUPL1 in diagram
-- ==========================================
CREATE DATABASE IF NOT EXISTS `lumiere_supplier`;
USE `lumiere_supplier`;

CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50),
    contact_email VARCHAR(100),
    contact_phone VARCHAR(20),
    address TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS supplier_products (
    sp_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT NOT NULL,
    product_ref_id INT NOT NULL,        -- Reference to lumiere_tenant_1.products
    supply_price DECIMAL(15,2) NOT NULL,
    min_order_qty INT DEFAULT 1,
    lead_time_days INT DEFAULT 3,       -- Days to deliver to warehouse
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

CREATE TABLE IF NOT EXISTS purchase_orders (
    po_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT NOT NULL,
    total_amount DECIMAL(15,2) NOT NULL,
    status ENUM('draft','sent','confirmed','delivered','cancelled') DEFAULT 'draft',
    expected_delivery DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

CREATE TABLE IF NOT EXISTS po_items (
    po_item_id INT AUTO_INCREMENT PRIMARY KEY,
    po_id INT NOT NULL,
    product_ref_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(15,2) NOT NULL,
    FOREIGN KEY (po_id) REFERENCES purchase_orders(po_id)
);

-- Seed data (matches lumiere_tenant_1 suppliers)
INSERT INTO suppliers (supplier_name, category, contact_email, contact_phone) VALUES
('Global Components Inc.', 'Electronics', 'global@supplier.com', '021-5550001'),
('North Star Textiles', 'Apparel', 'northstar@supplier.com', '021-5550002'),
('Summit Woodworks', 'Furniture', 'summit@supplier.com', '021-5550003'),
('Horizon Chemicals', 'Beauty', 'horizon@supplier.com', '021-5550004'),
('Apex Sports Gear', 'Sports', 'apex@supplier.com', '021-5550005'),
('Zenith Publishing', 'Books', 'zenith@supplier.com', '021-5550006');
