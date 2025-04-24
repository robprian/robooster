# Tahap build untuk backend
FROM python:3.11-slim as backend-builder
WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend .

# Tahap build untuk bot
FROM python:3.11-slim as bot-builder
WORKDIR /app/bot
COPY bot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY bot .

# Tahap final
FROM python:3.11-slim
WORKDIR /app

# Copy dari builder stages
COPY --from=backend-builder /app/backend /app/backend
COPY --from=bot-builder /app/bot /app/bot
COPY deploy/start.sh /app/start.sh

# Install dependencies
RUN pip install --no-cache-dir supervisor

# Copy supervisor configuration
COPY deploy/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Make start script executable
RUN chmod +x /app/start.sh

EXPOSE 8000

# Start supervisor
CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]