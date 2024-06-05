CREATE DATABASE product_db;

USE product_db;

CREATE TABLE  products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name  VANCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    type VARCHAR(255) NOT NULL
);

INSERT INFO products(name,price,type) VALUES('EXAMPLE PRODUCT',100.00,'mmu stuff')