#!/bin/bash

npm i --prefix ./redttg_mail_frontend
pip install -r requirements.txt
python manage.py migrate
python manage.py shell < ".devcontainer/create-superuser.py"

sudo cp "$(dirname "$0")/nginx.conf" "/etc/nginx/conf.d/default.conf"