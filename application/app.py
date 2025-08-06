from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_mysqldb import MySQL
import db_config
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key=os.getenv("FLASK_SECRET_KEY")

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf','png','jpg','jpeg'}


# Configuring MySQL 
app.config['MYSQL_HOST'] = db_config.MYSQL_HOST
app.config['MYSQL_USER'] = db_config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = db_config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = db_config.MYSQL_DB
app.config['MYSQL_CURSORCLASS'] = db_config.MYSQL_CURSORCLASS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder if not exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
mysql =  MySQL(app)

@app.route("/")
def index():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        process_id = request.form.get('process_id')

        # Basic validation
        if not name or not email:
            flash('Name and Email are required.', 'error')
        elif not process_id:
            flash('Please select a process for assignment.', 'error')
        else:
            try:
                # Insert new customer
                cur.execute(
                    "INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)",
                    (name, email, phone)
                )
                customer_id = cur.lastrowid

                # Assign customer to the selected process
                cur.execute(
                    "INSERT INTO process_assignments (customer_id, process_id, status, completion_percentage) VALUES (%s, %s, %s, %s)",
                    (customer_id, process_id, 'pending', 0.0)
                )

                mysql.connection.commit()
                flash('Customer registered and assigned to process successfully!', 'success')
                return redirect(url_for('register'))
            except Exception as e:
                mysql.connection.rollback()
                flash(f'Error occurred: {str(e)}', 'error')

    # On GET or failed POST, fetch customers and active processes for the form
    cur.execute("SELECT * FROM customers ORDER BY registration_date DESC")
    customers = cur.fetchall()

    cur.execute("SELECT * FROM processes WHERE status = 'active' ORDER BY name")
    processes = cur.fetchall()
    
    return render_template('register.html', customers=customers, processes=processes)

@app.route("/submit_document", methods=['POST', 'GET'])
def submit_document():
    cur = mysql.connection.cursor()

    # Fetching customers, processes, document types for dropdowns
    cur.execute("SELECT id, name FROM customers ORDER BY id")
    customers = cur.fetchall()
    cur.execute("SELECT id, name FROM processes WHERE status = 'active' ORDER BY id")
    processes = cur.fetchall()
    cur.execute("SELECT id, document_name FROM document_types ORDER BY id")
    document_types = cur.fetchall()

    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        process_id = request.form.get('process_id')
        document_type_id = request.form.get('document_type_id')
        ocr_extracted_data = request.form.get('ocr_extracted_data', '{}')
        file = request.files.get('file')
        
        # Basic validation
        if not all([customer_id, process_id, document_type_id]):
            flash('Please select customer, process, and document type.', 'error')
        elif file is None or file.filename == '':
            flash('Please select a file to upload.', 'error')
        elif not allowed_file(file.filename):
            flash('File type not allowed. Allowed types: pdf, png, jpg, jpeg', 'error')
        
        else:
            try:
                # SAVe FILE
                filename = file.filename
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(save_path)

                # INSERT RECORDS IN DOCUMENT_SUBMISSIONS TABLE
                cur.execute("""
                INSERT INTO document_submissions
                (customer_id, process_id, document_type_id, file_url, ocr_extracted_data, validation_status)
                VALUES
                (%s, %s, %s, %s, %s, %s)
                """, (
                    customer_id,
                    process_id,
                    document_type_id,
                    '/' + save_path.replace('\\', '/'),  # URL path (relative)
                    ocr_extracted_data,
                    'pending'
                    ))

                mysql.connection.commit()
                flash('Document uploaded successfully!', 'success')

                return redirect(url_for('submit_document'))
            
            except Exception as e:
                mysql.connection.rollback()
                flash(f'Error saving document: {e}', 'error')

    return render_template('submit_document.html', customers=customers, processes=processes, document_types=document_types)

@app.route("/dashboard")
def dashboard():
    cur = mysql.connection.cursor()

     # Query to get process assignments with counts of submitted and required docs
    query = """
        SELECT
            pa.id AS assignment_id,
            c.name AS customer_name,
            p.name AS process_name,
            pa.status AS assignment_status,
            pa.completion_percentage,
            -- Count how many docs submitted for this customer/process
            (
                SELECT COUNT(*)
                FROM document_submissions ds
                WHERE ds.customer_id = pa.customer_id AND ds.process_id = pa.process_id
            ) AS docs_submitted
        FROM process_assignments pa
        JOIN customers c ON pa.customer_id = c.id
        JOIN processes p ON pa.process_id = p.id
        ORDER BY c.name, p.name;
    """

    cur.execute(query)
    assignments = cur.fetchall()

        # For each assignment, add a field to display doc submission status
    for a in assignments:
        a['docs_status'] = "Submitted" if a['docs_submitted'] > 0 else "None"

    return render_template('status_dashboard.html', assignments=assignments)

            
if __name__ == '__main__':
    app.run(debug=True)     