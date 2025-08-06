CREATE DATABASE Quickdocs;
USE Quickdocs;

DROP TABLE IF EXISTS document_submissions;
DROP TABLE IF EXISTS process_assignments;
DROP TABLE IF EXISTS document_types;
DROP TABLE IF EXISTS processes;
DROP TABLE IF EXISTS customers;

CREATE TABLE processes (
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(50) NOT NULL UNIQUE,
description text,
status ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE document_types (
id INT AUTO_INCREMENT PRIMARY KEY,
document_name VARCHAR(50) NOT NULL UNIQUE,
description text,
required_fields JSON NOT NULL
);

CREATE TABLE customers (
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(50) NOT NULL,
email VARCHAR(50) NOT NULL UNIQUE,
phone VARCHAR(15),
registration_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

create TABLE process_assignments(
id INT AUTO_INCREMENT PRIMARY KEY,
customer_id INT NOT NULL,
process_id INT NOT NULL,
assignment_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
status ENUM('pending','completed','in-progress') NOT NULL DEFAULT 'pending',
completion_percentage DECIMAL(5,2) DEFAULT 0.00,
FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE, 
FOREIGN KEY (process_id) REFERENCES processes(id) ON DELETE CASCADE
);

CREATE TABLE document_submissions (
id INT AUTO_INCREMENT PRIMARY KEY,
customer_id INT NOT NULL,
process_id INT NOT NULL,
document_type_id INT NOT NULL,
upload_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
file_url TEXT NOT NULL,
ocr_extracted_data JSON,
validation_status ENUM('pending','approved','rejected') NOT NULL DEFAULT 'pending',
FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
FOREIGN KEY (process_id) REFERENCES processes(id) ON DELETE CASCADE,
FOREIGN KEY (document_type_id) REFERENCES document_types(id) ON DELETE CASCADE
);

SELECT * from processes;
select * from document_types;
select * from customers;
select * from process_assignments;
select * from document_submissions;

SELECT id, name FROM customers ORDER BY id;
SELECT id, name FROM processes WHERE status = 'active' ORDER BY id;
SELECT id, document_name FROM document_types ORDER BY id;