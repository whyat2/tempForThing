-- Create databases for each app
CREATE DATABASE IF NOT EXISTS app1_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS app2_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create users for each app
CREATE USER 'app1_user'@'%' IDENTIFIED BY 'app1_pass';
CREATE USER 'app2_user'@'%' IDENTIFIED BY 'app2_pass';

-- Grant privileges
GRANT ALL PRIVILEGES ON *.* TO 'app1_user'@'%' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'app2_user'@'%' WITH GRANT OPTION;

-- Apply privileges
FLUSH PRIVILEGES;

-- Create tables
USE app1_db;
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

USE app2_db;
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
