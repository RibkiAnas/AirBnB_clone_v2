#!/usr/bin/python3
"""
Fabric script that deletes out-of-date
archives
"""
from fabric.api import *
from time import strftime
from datetime import datetime
import os


env.hosts = ["52.72.79.60", "100.25.136.86"]


def do_pack():
    """
    Generates a .tgz archive from the
    contents of the web_static folder
    """
    local("mkdir -p versions")
    now = datetime.now()
    archive_path = "web_static_{}.tgz".format(now.strftime("%Y%m%d%H%M%S"))
    if local("tar -czvf versions/{} web_static".format(archive_path)):
        return archive_path
    else:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to the web
    servers
    """
    if os.path.exists(archive_path) is False:
        return False
    try:
        """Get the file name without ext"""
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        """Upload the archive"""
        tar_file = put(archive_path, "/tmp/")
        if tar_file.failed:
            return False
        """Uncompress the archive"""
        tar_file = run("mkdir -p /data/web_static/releases/{}/".format(no_ext))
        if tar_file.failed:
            return False
        tar_file = run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
                       .format(file_name, no_ext))
        if tar_file.failed:
            return False
        """Delete the archive"""
        tar_file = run("rm /tmp/{}".format(file_name))
        if tar_file.failed:
            return False
        """Move contents to host web_static"""
        tar_file = run('mv /data/web_static/releases/{}/web_static/* \
                /data/web_static/releases/{}/'.format(no_ext, no_ext))
        if tar_file.failed:
            return False
        """Remove web_static dir"""
        tar_file = run('rm -rf /data/web_static/releases/{}/web_static'
                       .format(no_ext))
        if tar_file.failed:
            return False
        """Delete the symbolic link"""
        tar_file = run("rm -rf /data/web_static/current")
        if tar_file.failed:
            return False
        """Create a new symbolic link"""
        tar_file = run("ln -s /data/web_static/releases/{} \
                /data/web_static/current".format(no_ext))
        if tar_file.failed:
            return False
        print('New version deployed!')
        return True
    except Exception:
        return False


def deploy():
    """
    Deploy function that creates and
    distributes an archive
    """
    created_path = do_pack()
    if created_path is None:
        return False
    return do_deploy(created_path)


def do_clean(number=0):
    """Deletes out-of-date archives"""
    number = int(number)
    if number == 0 or number == 1:
        number = 1
    else:
        number += 1
    """Delete local archives"""
    local("cd versions ; ls -t | tail -n +{} | xargs rm -rf".format(number))
    """Delete remote archives"""
    run("cd /data/web_static/releases ; ls -t | tail -n +{} | xargs rm -rf"
        .format(number))
