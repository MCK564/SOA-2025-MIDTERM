#!/bin/bash

# --- 1. Chờ đợi Dependencies ---
echo "Checking all dependencies..."

# Chờ MySQL
while ! nc -z mysql 3306; do
  echo 'Waiting for MySQL (3306)...'; sleep 1;
done

# Chờ Redis
while ! nc -z redis 6379; do
  echo 'Waiting for Redis (6379)...'; sleep 1;
done

# Chờ Kafka
while ! nc -z kafka 9092; do
  echo 'Waiting for Kafka (9092)...'; sleep 1;
done

echo '✅ All dependencies are UP.'

# --- 2. Khởi động Ứng dụng (Sử dụng exec) ---
# Lệnh 'exec' thay thế shell script này bằng tiến trình uvicorn,
# đảm bảo Uvicorn là PID 1 và container chạy mãi.
echo "Starting Uvicorn..."
exec uvicorn main:app --host 0.0.0.0 --port 8003 --reload