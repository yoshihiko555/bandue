#!/usr/bin/bash

rm -rf ./api/migrations
rm -rf db.sqlite3

python manage.py makemigrations api

python manage.py migrate

python manage.py loaddata fixture-age.json
python manage.py create_admin
