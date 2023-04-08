#!/usr/python3

from fabric.api import env, local, put, run
from datetime import datetime
import os


env.user = 'ubuntu'  # the user to use for ssh
env.hosts = ['<IP web-01>', 'IP web-02']  # list of web servers IP addresses
env.key_filename = '~/.ssh/<private_key>'  # path to your private ssh key


def do_pack():
    """
    Generate a .tgz archive of the web_static folder.

    Returns:
        (str): path of the archive file if successful, None otherwise.
    """
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")

        now = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = "versions/web_static_" + now + ".tgz"

        local("tar -czvf {} web_static".format(file_name))

        return file_name

    except Exception:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to web servers.

    Args:
        archive_path (str): path of the archive file to distribute.

    Returns:
        True if successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        file_name = os.path.basename(archive_path).split(".")[0]

        put(archive_path, "/tmp/")

        run("mkdir -p /data/web_static/releases/{}/".format(file_name))

        run("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/"
            .format(file_name, file_name))

        run("rm /tmp/{}.tgz".format(file_name))

        run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/"
            .format(file_name, file_name))

        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(file_name))

        run("rm -rf /data/web_static/current")

        run("ln -s /data/web_static/releases/{}/ "
            "/data/web_static/current".format(file_name))

        print("New version deployed!")

        return True

    except Exception:
        return False


def deploy():
    """
    Full deployment: pack the web_static folder and distribute the archive
    to web servers.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)


