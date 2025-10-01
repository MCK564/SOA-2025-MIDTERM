#!/bin/sh
# file: init-kafka.sh

echo "Waiting for Kafka to be ready..."
# Lặp lại cho đến khi kết nối được với Kafka
cub kafka-ready -b kafka:9092 1 20

echo "Kafka is ready. Creating topics..."
# Tạo topic otp_emails
kafka-topics --create --if-not-exists --topic otp_emails --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1

echo "Topics created successfully."