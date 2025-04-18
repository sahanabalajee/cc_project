import time
import json
import logging
from kafka import KafkaProducer
from kafka.errors import KafkaError

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - PRODUCER - %(levelname)s - %(message)s')
LOG_FILE_PATH = "/app/app.log"

# --- Kafka Configuration ---
KAFKA_BROKER = 'kafka:29092'
LOG_TOPIC = 'application-logs'

# --- Create Kafka Producer ---
def create_kafka_producer():
    logging.info(f"Connecting to Kafka at {KAFKA_BROKER}...")
    producer = None
    retries = 5
    while retries > 0 and producer is None:
        try:
            producer = KafkaProducer(
                bootstrap_servers=[KAFKA_BROKER],
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                retries=3,
                linger_ms=100,
                batch_size=16384
            )
            logging.info("Kafka producer connected.")
        except KafkaError as e:
            logging.error(f"Kafka connection error: {e}. Retrying...")
            retries -= 1
            time.sleep(5)
    if not producer:
        logging.error("Could not connect to Kafka. Exiting.")
        exit(1)
    return producer
def tail_log_file(path):
    with open(path, "r") as f:
        f.seek(0, 2)  # Go to end of file
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            yield line.strip()

# --- Send a log message to Kafka ---
def send_log(producer, topic, message):
    producer.send(topic, {"raw_log": message})
    logging.info(f"[PRODUCER] Sent: {message}")

# --- Main Loop (placeholder) ---
if __name__ == "__main__":
    kafka_producer = create_kafka_producer()

    logging.info("Kafka producer is running. Awaiting logs... (simulate or integrate input here)")
    try:
        # Simulate logs (you can replace this with input from file, HTTP, etc.)
        while True:
            for log_line in tail_log_file(LOG_FILE_PATH):
                send_log(kafka_producer, LOG_TOPIC, log_line)
    except KeyboardInterrupt:
        logging.info("Shutting down producer...")
    finally:
        kafka_producer.flush()
        kafka_producer.close()
        logging.info("Producer closed.")
