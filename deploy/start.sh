#!/bin/bash

# Tunggu PostgreSQL siap
until pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER
do
  echo "Menunggu PostgreSQL siap..."
  sleep 2
done

# Jalankan migrasi database
cd /app/backend
python -c "from models import Base, engine; Base.metadata.create_all(engine)"

# Jalankan supervisord
exec /usr/local/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf