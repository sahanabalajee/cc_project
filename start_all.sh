#!/bin/bash

echo "Starting docker containers..."
docker-compose up -d

sleep 5

echo "Starting API server..."

sleep 2

echo "Starting Kafka producer..."
python3 kafka_producer.py &

sleep 2

echo "Starting Workload Simulator..."
python3 workload_simulator.py &

sleep 2

echo "Starting Kafka Consumer..."
python3 kafka_consumer.py &

echo "✅ All services started!"
