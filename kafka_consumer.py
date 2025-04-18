import json
import psycopg2
from kafka import KafkaConsumer
import logging
import re
from datetime import datetime

KAFKA_BROKER = 'kafka:29092'
KAFKA_TOPIC = 'application-logs'

# Postgres Config
DB_NAME = 'applogsdb'
DB_USER = 'root'
DB_PASS = 'apppassword'
DB_HOST = 'postgres'
DB_PORT = '5432'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()
def parse_log(log):
    """
    Parses log lines like: "GET /users 200 23ms"
    """
    pattern = r'(?P<method>GET|POST|PUT|DELETE) (?P<endpoint>/\S*) (?P<status>\d{3}) (?P<time>\d+)ms'
    match = re.search(pattern, log)
    if match:
        return {
            "endpoint": match.group("endpoint"),
            "status_code": int(match.group("status")),
            "response_time_ms": float(match.group("time"))
        }
    return None

# Setup Kafka Consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - CONSUMER - %(levelname)s - %(message)s')

# Consume messages
try:
    logging.info(f"Starting Kafka consumer on topic '{KAFKA_TOPIC}'...")
    for message in consumer:
        log_entry = message.value.get('raw_log', '') 
        parsed = parse_log(log_entry) # Read the raw log
        logging.info(f"Consumed log: {log_entry}")
        #logging.info(f"parsed log: {parsed}")
        if parsed:
            cursor.execute(
            """
            INSERT INTO logs (raw_log, received_at, endpoint, status_code, response_time_ms)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                log_entry,
                datetime.now(),
                parsed["endpoint"],
                parsed["status_code"],
                parsed["response_time_ms"]
            )
        )
            conn.commit()
            logging.info(f"Inserted log into DB: {log_entry}")
        

except KeyboardInterrupt:
    logging.info("Shutting down consumer...")

finally:
    # Always close in finally so it happens even if error
    consumer.close()
    cursor.close()
    conn.close()
    logging.info("Kafka consumer and database connections closed.")
