FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y netcat-openbsd --no-install-recommends && rm -rf /var/lib/apt/lists/*


COPY . .
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh # Cấp quyền thực thi
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003",  "--reload"]
