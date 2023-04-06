#!/usr/bin/env python
"""
Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo, using the function do_pack.
"""

from fabric.api import local, env
from datetime import datetime


env.hosts = ['localhost']


def do_pack():
    try:
        current_time = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        archive_path = "versions/web_static_{}.tgz".format(current_time)
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except:
        return None

