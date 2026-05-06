-- ==========================================
-- WEEK 1: DATABASE ARCHITECTURE (VERSION A - ISOLATED)
-- Project: Lumiere E-Commerce Ecosystem
-- Target Database: lumiere_tenant_1
-- ==========================================

-- 1. Create and Use the isolated database for Tenant 1
CREATE DATABASE IF NOT EXISTS `lumiere_tenant_1`;
USE `lumiere_tenant_1`;

-- ==========================================
-- SCHEMA DEFINITION (NO tenant_id NEEDED HERE)
-- ==========================================

-- 1. Users (Buyers for this specific tenant)
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Fintech Institutions
CREATE TABLE IF NOT EXISTS fintech_institutions (
    institution_id INT AUTO_INCREMENT PRIMARY KEY,
    institution_name VARCHAR(100) NOT NULL UNIQUE,
    api_endpoint VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE
);

-- 3. Shipping Companies
CREATE TABLE IF NOT EXISTS shipping_companies (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL UNIQUE,
    contact_number VARCHAR(20)
);

-- 4. Suppliers
CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50)
);

-- 5. Products (Purely isolated for Tenant 1)
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(15, 2) NOT NULL,
    stock INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Orders
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    buyer_id INT NOT NULL,
    institution_id INT,
    total_amount DECIMAL(15, 2) NOT NULL,
    order_status ENUM('order', 'pay', 'delivery', 'cancel', 'return') DEFAULT 'order',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX (buyer_id),
    FOREIGN KEY (buyer_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (institution_id) REFERENCES fintech_institutions(institution_id)
);

-- 7. Order Items
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price_at_purchase DECIMAL(15, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);

-- 8. Shipping Tracking
CREATE TABLE IF NOT EXISTS shipping_tracking (
    tracking_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    company_id INT NOT NULL,
    tracking_number VARCHAR(100),
    shipping_status VARCHAR(50) DEFAULT 'Preparing',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES shipping_companies(company_id) ON DELETE CASCADE
);

-- ==========================================
-- MOCK DATA (Satisfying Business Rules)
-- ==========================================

-- Shipping & Fintech
INSERT INTO shipping_companies (company_name, contact_number) VALUES
('Velocity Express', '555-0101'), ('Swift Global Logistics', '555-0102'),
('Blue Ridge Shipping', '555-0103'), ('Atlantic Freight', '555-0104'),
('Pacific Courier', '555-0105'), ('Peak Performance Delivery', '555-0106'),
('Silver Bullet Logistics', '555-0107'), ('Northern Star Express', '555-0108'),
('Mountain West Shippers', '555-0109'), ('Golden State Carriers', '555-0110'),
('Ironclad Logistics', '555-0111'), ('Liberty Express', '555-0112'),
('Freedom Freight', '555-0113'), ('Patriot Delivery', '555-0114'),
('Empire Shipping', '555-0115'), ('Frontier Logistics', '555-0116');

INSERT INTO fintech_institutions (institution_name, api_endpoint) VALUES
('Apex Finance', 'https://api.apexfinance.com'),
('Summit Capital', 'https://api.summitcap.com'),
('Horizon Payments', 'https://api.horizonpay.com'),
('Zenith Banking', 'https://api.zenithbank.com'),
('Sterling Fintech', 'https://api.sterlingfin.com');

-- Suppliers (Min 6 for this tenant)
INSERT INTO suppliers (supplier_name, category) VALUES
('Global Components Inc.', 'Electronics'), ('North Star Textiles', 'Apparel'),
('Summit Woodworks', 'Furniture'), ('Horizon Chemicals', 'Beauty'),
('Apex Sports Gear', 'Sports'), ('Zenith Publishing', 'Books');

-- Buyers (Min 10)
DELIMITER //
CREATE PROCEDURE PopulateBuyers()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= 10 DO
        INSERT INTO users (username, email, password_hash, first_name, last_name)
        VALUES (CONCAT('isolated_buyer_', i), CONCAT('buyer', i, '@isolated.com'), 'pw', 'User', i);
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;
CALL PopulateBuyers();
DROP PROCEDURE PopulateBuyers;

-- Products (Min 30)
DELIMITER //
CREATE PROCEDURE PopulateProducts()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= 30 DO
        INSERT INTO products (product_name, description, price, stock)
        VALUES (CONCAT('Isolated Item ', i), 'Premium quality for Version A', ROUND(RAND() * 200 + 20, 2), 50);
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;
CALL PopulateProducts();
DROP PROCEDURE PopulateProducts;

-- Transactions (Min 100)
DELIMITER //
CREATE PROCEDURE PopulateOrders()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= 100 DO
        INSERT INTO orders (buyer_id, institution_id, total_amount, order_status)
        VALUES ((i % 10) + 1, (i % 5) + 1, ROUND(RAND() * 500 + 50, 2), 'pay');
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;
CALL PopulateOrders();
DROP PROCEDURE PopulateOrders;
