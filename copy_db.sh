#!/usr/bin/env bash

set -u

if [[ $# -ne 2 ]]; then
    printf "usage: %s SRC_DB DEST_DB" "$(basename "$0")"
    exit 1
fi

SRC_DB=$1
DEST_DB=$2

echo "Creating \"$DEST_DB\""
dropdb --if-exists $DEST_DB && createdb $DEST_DB
pg_dump --schema-only $SRC_DB | psql $DEST_DB

# Tables safe to copy as is
COPY="batch drug_class drug dose_unit ethnicity apoe race country time_unit \
      lab_unit lab_test arm"
for TABLE in $COPY; do
    echo "Copying \"$TABLE\""
    pg_dump --data-only $SRC_DB -t $TABLE | psql $DEST_DB
done

echo "Done."
