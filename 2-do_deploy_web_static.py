#!/usr/bin/python3
"""A script to distribute archives to servers"""
from os.path import exists
from fabric.api import run, put, env

env.hosts = ["34.207.221.236", "54.160.82.203"]


def do_deploy(archive_path):
    """Deploy to the webserver"""
    if not exists(archive_path):
        return False

    fname = archive_path.split("/")[1]
    flname = archive_path.split("/")[1].split(".")[0]

    if put(archive_path, "/tmp/{}".format(
           fname)).failed is True:
        return False

    if run("rm -rf /data/web_static/releases/{}/".format(
           flname)).succeeded is False:
        return False

    if run("mkdir -p /data/web_static/releases/{}/".format(
           flname)).succeeded is False:
        return False

    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
           fname, flname)).succeeded is False:
        return False

    if run("rm /tmp/{}".format(fname)).failed is True:
        return False

    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(flname, flname)
           ).failed is True:
        return False

    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(flname)).failed is True:
        return False

    if run("rm -rf /data/web_static/current").failed is True:
        return False

    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(flname)).succeeded is False:
        return False

    return True
