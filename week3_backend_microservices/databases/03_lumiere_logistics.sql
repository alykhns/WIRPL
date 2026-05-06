-- ==========================================
-- LUMIERE LOGISTICS SERVICE DATABASE
-- Equivalent to: Shipping tracking in diagram
-- ==========================================
CREATE DATABASE IF NOT EXISTS `lumiere_logistics`;
USE `lumiere_logistics`;

CREATE TABLE IF NOT EXISTS couriers (
    courier_id INT AUTO_INCREMENT PRIMARY KEY,
    courier_name VARCHAR(100) NOT NULL,     -- JNE, SiCepat, J&T
    service_type VARCHAR(50),               -- Regular, Express, Same Day
    cost_per_km DECIMAL(10,2) DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS shipments (
    shipment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,              -- Reference to lumiere_tenant_1.orders
    courier_id INT NOT NULL,
    tracking_number VARCHAR(100) UNIQUE,
    origin_address TEXT,
    destination_address TEXT,
    shipping_status ENUM('preparing','picked_up','in_transit','delivered','returned') DEFAULT 'preparing',
    estimated_delivery DATE,
    actual_delivery TIMESTAMP NULL,
    shipping_cost DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (courier_id) REFERENCES couriers(courier_id)
);

CREATE TABLE IF NOT EXISTS tracking_history (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    shipment_id INT NOT NULL,
    location VARCHAR(255),
    status_note VARCHAR(255),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id)
);

-- Seed data
INSERT INTO couriers (courier_name, service_type, cost_per_km) VALUES
('JNE', 'Regular', 1500),
('JNE', 'Express', 2500),
('SiCepat', 'Regular', 1400),
('SiCepat', 'BEST', 2000),
('J&T Express', 'Regular', 1300),
('GoSend', 'Same Day', 5000),
('Anteraja', 'Regular', 1200);
