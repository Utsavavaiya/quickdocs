USE quickdocs;

-- Sample Processes
INSERT INTO processes (name, description, status) VALUES
('Loan Application', 'Applying for a personal loan', 'active'),
('KYC Verification', 'Customer KYC check', 'active');

-- Sample Document Types with required_fields as JSON
INSERT INTO document_types (document_name, description, required_fields) VALUES
('PAN Card', 'Permanent account number card', JSON_OBJECT('fields', JSON_ARRAY('full_name','pan_number','dob'))),
('Salary Slip', 'Monthly salary slip', JSON_OBJECT('fields', JSON_ARRAY('employee_name','salary','month'))),
('Bank Statement', 'Account statement', JSON_OBJECT('fields', JSON_ARRAY('account_number','bank_name','period'))),
('Aadhaar Card', 'Indian Aadhaar identity', JSON_OBJECT('fields', JSON_ARRAY('aadhaar_number','dob'))),
('Address Proof', 'Document for address verification', JSON_OBJECT('fields', JSON_ARRAY('address_line1','city','zip')));

-- Sample Customers
INSERT INTO customers (name, email, phone) VALUES
('Rajesh Patel', 'rajesh.patel@email.com', '9112345678'),
('Priya Sharma', 'priya.sharma@email.com', '9112345679'),
('Amit Kumar',  'amit.kumar@email.com',  '9112345680'),
('Sonal Mehta', 'sonal.mehta@email.com', '9112345681'),
('Krish Rao',   'krish.rao@email.com',   '9112345682');

-- Sample Process Assignments (customer to process)
INSERT INTO process_assignments (customer_id, process_id, status, completion_percentage) VALUES
(1, 1, 'pending', 40.00),    -- Rajesh assigned to Loan Application
(2, 1, 'pending', 20.00),    -- Priya assigned to Loan Application
(3, 2, 'completed', 100.00), -- Amit assigned to KYC Verification
(4, 2, 'pending', 10.00),    -- Sonal assigned to KYC Verification
(5, 1, 'pending', 0.00);     -- Krish assigned to Loan Application

-- Sample Document Submissions
INSERT INTO document_submissions (customer_id, process_id, document_type_id, file_url, ocr_extracted_data, validation_status)
VALUES
-- Rajesh's PAN
(1, 1, 1, '/files/rajesh_pan.pdf', JSON_OBJECT('full_name','Rajesh Patel','pan_number','ABCDE1234F','dob','1982-05-01'), 'approved'),
-- Priya's Salary Slip
(2, 1, 2, '/files/priya_salary.pdf', JSON_OBJECT('employee_name','Priya Sharma','salary',55000,'month','04-2024'), 'pending'),
-- Amit's Aadhaar
(3, 2, 4, '/files/amit_aadhaar.pdf', JSON_OBJECT('aadhaar_number','123412341234','dob','1978-03-16'), 'approved'),
-- Sonal's Bank Statement
(4, 2, 3, '/files/sonal_bank.pdf', JSON_OBJECT('account_number','200300400','bank_name','SBI','period','Q1-2024'), 'rejected'),
-- Krish's Address Proof
(5, 1, 5, '/files/krish_address.pdf', JSON_OBJECT('address_line1','123 MG Road','city','Bangalore','zip','560001'), 'pending');
