#!/bin/bash

sudo apt-get update
sudo apt-get install nginx -y

cp "$(dirname "$0")/nginx.conf" "/etc/nginx/conf.d/default.conf"