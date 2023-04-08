#!/usr/bin/env bash
# This script sets up web servers for deployment of web_static.


if ! command -v nginx >/dev/null; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

sudo mkdir -p /data/web_static/{releases,test,shared}
sudo echo "<html><head></head><body>Holberton School</body></html>" | sudo tee /data/web_static/releases/test/index.html >/dev/null
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

STATIC_CONFIG="location /hbnb_static {\n\talias /data/web_static/current/;\n}\n"
sudo sed -i "s/# server_name_in_redirect off;/server_name_in_redirect off;\n\n$STATIC_CONFIG/" /etc/nginx/sites-available/default
sudo service nginx restart

