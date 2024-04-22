#!/bin/bash

set -e

while ! pg_isready -U $POSTGRES_USER -d $POSTGRES_DB; do
  sleep 1
  echo "Waiting for postgres to be ready..."
done

psql -U $POSTGRES_USER -d $POSTGRES_DB -f /etc/app/database.ddl