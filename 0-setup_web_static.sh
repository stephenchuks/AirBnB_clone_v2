#!/usr/bin/env bash

# Install Nginx if it's not already installed
if ! [ -x "$(command -v nginx)" ]; then
  apt-get update
  apt-get -y install nginx
fi

# Create necessary directories
mkdir -p /data/web_static/{releases/test,shared}

# Create a fake HTML file
echo "<html><head></head><body>Holberton School</body></html>" > /data/web_static/releases/test/index.html

# Create a symbolic link
if [ -h /data/web_static/current ]; then
  unlink /data/web_static/current
fi
ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group
chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration file
sed -i '/^\tserver_name _;/a \\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

# Restart Nginx
service nginx restart

exit 0


