import flask
import json
import time
import random
import logging
from flask import Flask, request, jsonify

# Configure basic logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(message)s'
)
app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_users():
    #logging.info(f"Request received for /users")
    # Simulate some processing time
    time.sleep(random.uniform(0.1, 0.3))
    users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    #logging.info(f"Request /users completed in {response_time:.4f} seconds")
    return jsonify(users)

@app.route('/products', methods=['GET'])
def get_products():
    start_time = time.time()
    logging.info(f"Request received for /products")
    # Simulate potential error
    if random.random() < 0.1: # 10% chance of error
        time.sleep(random.uniform(0.05, 0.1))
        response_time = time.time() - start_time
        #logging.error(f"Failed request /products in {response_time:.4f} seconds - Internal Server Error")
        return jsonify({"error": "Internal Server Error"}), 500
    else:
        # Simulate processing time
        time.sleep(random.uniform(0.2, 0.5))
        products = [{"id": 101, "name": "Laptop"}, {"id": 102, "name": "Mouse"}]
        response_time = time.time() - start_time
        logging.info(f"Request /products completed in {response_time:.4f} seconds")
        return jsonify(products)

@app.route('/orders', methods=['POST'])
def create_order():
    start_time = time.time()
    logging.info(f"Request received for /orders")
    try:
        data = request.get_json()
        if not data or 'product_id' not in data or 'quantity' not in data:
            response_time = time.time() - start_time
            logging.warning(f"Failed request /orders in {response_time:.4f} seconds - Bad Request: Missing data")
            return jsonify({"error": "Bad Request"}), 400

        # Simulate processing time
        time.sleep(random.uniform(0.3, 0.6))
        order_id = random.randint(1000, 9999)
        response_time = time.time() - start_time
        logging.info(f"Request /orders completed in {response_time:.4f} seconds - Order {order_id} created")
        return jsonify({"order_id": order_id, "status": "created"}), 201
    except Exception as e:
        response_time = time.time() - start_time
        logging.error(f"Failed request /orders in {response_time:.4f} seconds - Exception: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    start_time = time.time()
    logging.info(f"Request received for /health")
    response_time = time.time() - start_time
    logging.info(f"Request /health completed in {response_time:.4f} seconds")
    return jsonify({"status": "UP"})

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def log_request(response):
    if not hasattr(request, "start_time"):
        return response

    duration = time.time() - request.start_time
    log_msg = f"{request.method} {request.path} {response.status_code} {int(duration * 1000)}ms"
    app.logger.info(log_msg)
    return response

#if __name__ == '__main__':
    # Note: Using Flask's development server is not recommended for production.
    # Consider using a production-ready WSGI server like Gunicorn.
    #app.run(host='0.0.0.0', port=3000, debug=True) # Runs on port 5000