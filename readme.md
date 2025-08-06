# For Database Schema & Assets

This project includes all the assets you need to get up and running with the QuickDocs database:

### 1. Database Schema (`schema.sql`)
- Defines all necessary tables, columns, data types, relationships, and constraints.
- Ensures the structure matches what's required by the application (see the ER diagram below).
- **Setup:**  
  Run this file in your MySQL server to create all tables, including:
  - `processes`
  - `document_types`
  - `customers`
  - `process_assignments`
  - `document_submissions`
- Includes commands for initial SELECT queries to view table data.

### 2. Sample Data (`sample_data.sql`)
- Populates the database with realistic test data for instant experimentation.
- Includes:
  - Sample processes (e.g., "Loan Application", "KYC Verification").
  - Document types with their required fields as JSON (e.g., PAN Card, Aadhaar Card).
  - Sample customers, process assignments, and document submissions.
- **Usage:**  
  Run this after the schema has been set up to auto-populate your database and see the app in action immediately.

### 3. Entity Relationship Diagram (`er_diagram.jpg`)
- Visual representation of how tables connect and interact:
  - Shows primary and foreign key relationships.
  - Illustrates the one-to-many relations (for example, one customer can have many process assignments).
- **Usage:**  
  Refer to this diagram for a quick conceptual overview of the database design when troubleshooting or developing new features.

---

### Database Setup Instructions

1. **Create the database and tables:**

mysql -u <user> -p < schema.sql


2. **Insert the sample data:**

mysql -u <user> -p < sample_data.sql


3. **Verify your tables and data**  
Use the SELECT statements in `schema.sql` or a MySQL client to check that tables and data are loaded as expected.

---

**Note:**  
Be careful not to run the schema file on a database with important existing data—it will overwrite tables!

You can adjust the paths or descriptions if your files or table names differ. If you place this section after your "Technologies Used" section, it will make your README informative and helpful for new developers or users setting up your application!

---------------------------------------------------------------------------------------------------

# For QuickDocs Process & Document Management Application

A Flask-based application for registering customers, assigning processes, uploading and tracking documents, and viewing dashboard statuses for process assignments.

---

## Setup Instructions


2. **Install and activate a virtual environment (optional but recommended)**

python -m venv venv
source venv/bin/activate # On Unix/Mac
venv\Scripts\activate # On Windows


3. **Install required dependencies**

pip install -r requirements.txt

*Dependencies needed:*
- Flask
- Flask-MySQLdb
- python-dotenv

4. **Set up your `.env` file**

Create a `.env` file in your project directory with the following content. Replace values as needed:

FLASK_SECRET_KEY=your_flask_secret_key_here
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=quickdocs
MYSQL_CURSORCLASS=DictCursor


5. **Database Setup**
- Make sure you have a MySQL server running.
- Create the database and required tables (customers, processes, process_assignments, document_types, document_submissions).
- Update the names in `db_config.py` or `.env` if necessary.

---

## How to Run the Application

1. **Activate your virtual environment if not already active**
2. **Start the Flask app**
3. **Access the app**
Visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## API Keys Needed

- **FLASK_SECRET_KEY**
- Used for session management and flash messaging.
- **MySQL Credentials**
- `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB`, and `MYSQL_CURSORCLASS` (set in `.env`).
- **Note:** Do **not** include real secrets or passwords in public repositories. Use placeholder text where appropriate.

---

## Technologies Used

- **Python 3.x** — main programming language.
- **Flask** — micro web framework for handling server and routing.
- **Flask-MySQLdb** — MySQL integration for Flask.
- **python-dotenv** — loading sensitive config from `.env` files.
- **MySQL** — backend relational DBMS.
- **HTML/CSS (Jinja2 templates)** — for frontend UI and rendering.

---

## Notes

- Make sure your `UPLOAD_FOLDER` exists and is writable; it is set as `static/uploads` by default.
- Only certain file types (pdf, png, jpg, jpeg) are allowed for upload.
- Do not share or commit your `.env` file with real credentials to public repositories.

---------------------------------------------------------------------------------------------------------------------------------

# For NL-to-SQL Converter

An intuitive tool that converts natural language questions into accurate MySQL SQL queries for seamless database access.

## Setup Instructions

1. **Create and activate a virtual environment (recommended)**

python -m venv venv
source venv/bin/activate # On Unix or MacOS
venv\Scripts\activate # On Windows


2. **Install required Python dependencies**

pip install -r requirements.txt


3. **Set up your environment variables**
- Create a `.env` file in your root directory with the following, replacing placeholder values as appropriate:
  ```
  OPENAI_API_KEY=your_openai_api_key
  MYSQL_HOST=localhost
  MYSQL_USER=root
  MYSQL_PASSWORD=your_db_password
  MYSQL_DATABASE=quickdocs
  ```
- **Do not include actual API keys in this file if sharing it publicly.**

4. **Ensure your MySQL database is running and contains the required schema (see `main.py`).**

## How to Run the Application

1. Ensure your virtual environment is active.
2. Run the main program:

python query_interface.py

3. When prompted, enter a natural language query (e.g., "Show all customers registered after July 2024").
4. The application will:
- Generate the equivalent SQL query using the OpenAI API.
- Execute the SQL (if it's a SELECT statement).
- Display results in a readable table format.

## API Keys Needed

- **OpenAI API Key (`OPENAI_API_KEY`):**
- Required for accessing the GPT model for NL-to-SQL conversion.
- **MySQL Credentials:**
- Database host, user, password, and database name are required as environment variables.
- *Do not share actual sensitive credentials in the README or public repositories!*

## Technologies Used

- **Python 3.x** — for application logic
- **OpenAI GPT (via openai Python SDK)** — for NL-to-SQL query generation
- **mysql-connector-python** — for connecting and interacting with the MySQL database
- **python-dotenv** — for managing environment variables
- **MySQL** — as the backend relational database

## NL to SQL Conversion: How It Works

1. **Input:** User provides a natural language question via the console.
2. **Prompting:** The application constructs a prompt that includes the complete database schema and the user's question.
3. **Model Call:** This prompt is sent to the OpenAI GPT model which is instructed to return only the valid MySQL SQL query (no explanations).
4. **Post-processing:** If the model includes any formatting (like markdown), the code strips it to ensure only raw SQL is executed.
5. **Execution:** For `SELECT` queries, the SQL is executed against the specified MySQL database, and results are presented in a tabulated format.
6. **Safety:** Only `SELECT` statements are run by default for demo safety; other query types are acknowledged but not executed.

## Example of Successful Queries

![alt text](<image1.jpg>)

## Example of Error Handling

![alt text](<image2.jpg>)

---

**Note:** Never expose actual API keys or sensitive credentials in your README or public codebases. Replace them with placeholders as shown above.


