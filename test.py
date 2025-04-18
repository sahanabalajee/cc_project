import psycopg2
import logging

# Set up logging to print messages to the console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# PostgreSQL Connection Test
try:
    conn = psycopg2.connect(
        dbname='applogsdb',
        user='postgres',
        password='apppassword',
        host='localhost',
        port='5432'
    )
    logging.info("Connected to PostgreSQL successfully.")
except Exception as e:
    logging.error(f"Error connecting to PostgreSQL: {e}")

try:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_table (
            id SERIAL PRIMARY KEY,
            name TEXT
        )
    ''')
    conn.commit()
    logging.info("Test table created successfully.")
except Exception as e:
    logging.error(f"Error creating test table: {e}")
try:
    cursor.execute("INSERT INTO test_table (name) VALUES (%s)", ("Test Name",))
    conn.commit()
    logging.info("Data inserted into test table successfully.")
except Exception as e:
    logging.error(f"Error inserting data into test table: {e}")

try:
    cursor.execute("SELECT * FROM test_table;")
    rows = cursor.fetchall()
    logging.info(f"Data in test table: {rows}")
except Exception as e:
    logging.error(f"Error querying data: {e}")

