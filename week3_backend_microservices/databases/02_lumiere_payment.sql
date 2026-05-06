-- ==========================================
-- LUMIERE PAYMENT SERVICE DATABASE
-- Equivalent to: OVO / BankA in diagram
-- ==========================================
CREATE DATABASE IF NOT EXISTS `lumiere_payment`;
USE `lumiere_payment`;

CREATE TABLE IF NOT EXISTS payment_methods (
    method_id INT AUTO_INCREMENT PRIMARY KEY,
    method_name VARCHAR(50) NOT NULL,   -- e-wallet, bank_transfer, cod
    provider VARCHAR(100),              -- OVO, BCA, Mandiri, etc.
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS payment_transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,              -- Reference to lumiere_tenant_1.orders
    method_id INT NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    status ENUM('pending','success','failed','refunded') DEFAULT 'pending',
    external_ref VARCHAR(255),          -- OVO/bank transaction ref
    paid_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (method_id) REFERENCES payment_methods(method_id)
);

CREATE TABLE IF NOT EXISTS refunds (
    refund_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT NOT NULL,
    refund_amount DECIMAL(15,2) NOT NULL,
    reason TEXT,
    status ENUM('pending','processed','rejected') DEFAULT 'pending',
    processed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (transaction_id) REFERENCES payment_transactions(transaction_id)
);

-- Seed data
INSERT INTO payment_methods (method_name, provider) VALUES
('e-wallet', 'OVO'),
('e-wallet', 'GoPay'),
('bank_transfer', 'BCA'),
('bank_transfer', 'Mandiri'),
('cod', 'Cash on Delivery');
