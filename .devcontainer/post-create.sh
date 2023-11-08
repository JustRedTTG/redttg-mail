#!/bin/bash

# Copy nginx.conf to the same directory as post-create.sh
cp "$(dirname "$0")/nginx.conf" "/etc/nginx/conf.d/default.conf"

# Install nginx
sudo apt-get update
sudo apt-get install nginx -y