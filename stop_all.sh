#!/bin/bash

echo "Stopping Python services..."
pkill -f api_server.py
pkill -f kafka_producer.py
pkill -f workload_simulator.py
pkill -f kafka_consumer.py

echo "Stopping Docker containers..."
docker-compose down

echo "🛑 All services stopped!"
