import os
import openai
import mysql.connector
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),  # default to 'localhost' if not set
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

SCHEMA = """
Database Schema:

Table: processes
- id: INT, auto-increment, primary key
- name: VARCHAR(50), unique, not null
- description: TEXT
- status: ENUM('active', 'inactive'), not null, default 'active'
- created_date: TIMESTAMP, not null, default current timestamp

Table: document_types
- id: INT, auto-increment, primary key
- document_name: VARCHAR(50), unique, not null
- description: TEXT
- required_fields: JSON, not null

Table: customers
- id: INT, auto-increment, primary key
- name: VARCHAR(50), not null
- email: VARCHAR(50), unique, not null
- phone: VARCHAR(15)
- registration_date: TIMESTAMP, not null, default current timestamp

Table: process_assignments
- id: INT, auto-increment, primary key
- customer_id: INT, not null, foreign key references customers(id) ON DELETE CASCADE
- process_id: INT, not null, foreign key references processes(id) ON DELETE CASCADE
- assignment_date: TIMESTAMP, not null, default current timestamp
- status: ENUM('pending', 'completed', 'in-progress'), not null, default 'pending'
- completion_percentage: DECIMAL(5,2), default 0.00

Table: document_submissions
- id: INT, auto-increment, primary key
- customer_id: INT, not null, foreign key references customers(id) ON DELETE CASCADE
- process_id: INT, not null, foreign key references processes(id) ON DELETE CASCADE
- document_type_id: INT, not null, foreign key references document_types(id) ON DELETE CASCADE
- upload_date: TIMESTAMP, not null, default current timestamp
- file_url: TEXT, not null
- ocr_extracted_data: JSON
- validation_status: ENUM('pending', 'approved', 'rejected'), not null, default 'pending'
"""

client = OpenAI(api_key=OPENAI_API_KEY)

def get_sql_from_gpt(nl_query):
    prompt=f""" You are an intelligent SQL generator assistant.

    You will be given:
    - A database schema
    - A natural language question
    Your task is to return only the **valid MySQL SQL query** (no explanations, no headings, no markdown formatting like ```sql).

    Return the output as plain text — just the SQL.
    
    Here is the Schema: 

    {SCHEMA}

    Now convert the following question into a MySQL query:

    "{nl_query}"

    Output only the SQL query.
    """

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role":"user", "content":prompt}
        ],
        max_tokens=200,
        temperature=0.2
    )

    sql = response.choices[0].message.content.strip()
    
    if sql.startswith("```sql"):
        sql = sql.replace("```sql", "").replace("```", "").strip()
    elif sql.startswith("```"):
        sql = sql.replace("```", "").strip()

    return sql

def run_sql(sql):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        # print("DEBUG: Connected to DB")
        cur = conn.cursor(dictionary=True)
        sql = sql.strip().rstrip(';')
        # print("DEBUG: Executing SQL:", sql)
        cur.execute(sql)
        if cur.description:
            rows = cur.fetchall()
        else:
            rows = [{'RowsAffected': cur.rowcount}]
        # print("DEBUG inside run_sql: rows =", rows)
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("DEBUG: Exception occurred in run_sql()")
        print("DEBUG: Exception message:", e)
        return f"Database Error: {e}"

    
def pretty_print_table(rows):
    # print("DEBUG: Entered pretty_print_table")  # DEBUGGING 
    if not rows:
        print("(No results)")
        return
    headers = rows[0].keys()
    widths = [max(len(str(h)), max(len(str(r[k])) for r in rows)) for k, h in zip(headers, headers)]
    line = ' | '.join(h.ljust(w) for h, w in zip(headers, widths))
    print(line)
    print('-' * len(line))
    for row in rows:
        print(' | '.join(str(row[k]).ljust(w) for k, w in zip(headers, widths)))

if __name__ == "__main__":
    openai.api_key = OPENAI_API_KEY
    print("Quickdocs: NL2SQL (Type 'exit' to quit)\n")
    while True:
        nl_query = input("Enter your question: ").strip()
        if not nl_query or nl_query.lower() == 'exit':
            break
        print("\nGenerating SQL via OpenAI...")
        sql = get_sql_from_gpt(nl_query)

        print(f"\nGenerated SQL:\n{sql}\n")
        if sql.lower().startswith("select"):
            print("Executing query...")
            result = run_sql(sql)
            # print("DEBUG: SQL result:", result)
            # print("DEBUG: Type of result:", type(result))
            if isinstance(result, str):
                print(result)
            else:
                pretty_print_table(result)
        else:
            # Only support SELECT for safety in demo
            print("Only SELECT queries are executed for testing.")
        print("\n" + "="*60 + "\n")