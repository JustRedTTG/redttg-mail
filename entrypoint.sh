#!/bin/sh

echo "test"
exec "$@"
# echo "Waiting for postgres..."
# /app/wait-for-it.sh $DB_HOST:$DB_PORT -- /app/run.sh "$@"