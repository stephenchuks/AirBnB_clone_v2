#!/usr/bin/python3
"""
from fabric.api import local
from time import strftime
from datetime import date


def do_pack():
    """ This function generates archive of the contents of AirbnB web_static project in my repo"""

    fname = strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/"
              .format(fname))

        return "versions/web_static_{}.tgz".format(fname)

    except Exception as exc:
        return None
