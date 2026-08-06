#!/bin/bash
apk add --no-cache postgresql-client || true
createdb -U postgres all_in_one || true
for f in database/postgres/migrations/*.sql; do
    echo "Running $f"
    psql -v ON_ERROR_STOP=1 -U postgres -d all_in_one -f "$f" || { echo "Failed on $f"; break; }
done
