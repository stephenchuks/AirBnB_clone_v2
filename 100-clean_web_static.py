#!/usr/bin/python3
# This script deletes out of date archives
from fabric.api import local
from fabric.api import env
from fabric.api import run
from fabric.api import put
from datetime import datetime
import os.path

env.hosts = ['35.153.78.254', '54.160.73.228']


def do_clean(num=0):
    """Delete ood archives.
    """
    num = int(num)
    local("ls -d -1tr versions/* | tail -n +{} | \
          xargs -d '\n' rm -f --".format(2 if num < 1 else num + 1))
    run("ls -d -1tr /data/web_static/releases/* | tail -n +{} | \
          xargs -d '\n' rm -rf --".format(2 if num < 1 else num + 1))
