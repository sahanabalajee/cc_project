import requests
import time
import random
import logging

# Configure logging for the simulator
logging.basicConfig(level=logging.INFO, format='%(asctime)s - SIMULATOR - %(levelname)s - %(message)s')

API_BASE_URL = "http://localhost:3000" # URL of your Flask API server

ENDPOINTS = [
    {"path": "/users", "method": "GET"},
    {"path": "/products", "method": "GET"},
    {"path": "/orders", "method": "POST"},
    {"path": "/health", "method": "GET"},
    {"path": "/nonexistent", "method": "GET"} # Simulate a 404
]

HEADERS = {"Content-Type": "application/json"}

def make_request():
    endpoint_config = random.choice(ENDPOINTS)
    url = API_BASE_URL + endpoint_config["path"]
    method = endpoint_config["method"]
    payload = None

    try:
        start_time = time.time()
        response = None

        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            if endpoint_config["path"] == "/orders":
                # Send valid or invalid data randomly
                if random.random() < 0.8:
                    payload = {"product_id": random.randint(1, 100), "quantity": random.randint(1, 5)}
                else:
                    payload = {"product_id": random.randint(1, 100)} # Missing quantity
                response = requests.post(url, json=payload, headers=HEADERS, timeout=5)
            # Add other POST endpoints here if needed

        end_time = time.time()
        duration = end_time - start_time

        if response is not None:
            logging.info(f"{method} {url} - Status: {response.status_code} - Duration: {duration:.4f}s")
            # Optional: Log response body for debugging (can be verbose)
            # try:
            #     logging.debug(f"Response: {response.json()}")
            # except requests.exceptions.JSONDecodeError:
            #     logging.debug(f"Response (non-JSON): {response.text}")
        else:
             logging.warning(f"No response received for {method} {url}")

    except requests.exceptions.RequestException as e:
        end_time = time.time()
        duration = end_time - start_time
        logging.error(f"Request failed: {method} {url} - Error: {e} - Duration: {duration:.4f}s")
    except Exception as e:
         logging.error(f"An unexpected error occurred during request to {url}: {e}")


if __name__ == "__main__":
    logging.info("Starting workload simulator...")
    while True:
        make_request()
        # Wait for a random interval before the next request
        time.sleep(random.uniform(0.2, 1.5)) # Simulate variable load