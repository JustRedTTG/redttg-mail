#!/bin/bash

sudo apt-get update
sudo apt-get install nginx npm -y
npm i --prefix ./redttg_mail_frontend
pip install -r requirements.txt
python manage.py migrate

sudo cp "$(dirname "$0")/nginx.conf" "/etc/nginx/conf.d/default.conf"