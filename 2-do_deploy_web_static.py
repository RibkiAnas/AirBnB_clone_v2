#!/usr/bin/python3
"""
Fabric script that distributes
an archive to the web servers
"""
from fabric.api import *
import os


env.hosts = ["52.72.79.60", "100.25.136.86"]


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
