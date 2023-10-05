#!/usr/bin/python3
"""
Fabric script (based on the file
1-pack_web_static.py) that distributes an
archive to your web servers
"""
from fabric.api import *
from datetime import datetime
from os import path


env.hosts = ["52.72.79.60", "100.25.136.86"]


def do_deploy(archive_path):
    """
    Distributes an archive to the web
    servers
    """
    if not path.exists(archive_path):
        return False
    try:
        """Get the file name without ext"""
        file_name = path.basename(archive_path)
        no_ext = file_name.split(".")[0]
        """Upload the archive"""
        put(archive_path, "/tmp/")
        """Uncompress the archive"""
        run("mkdir -p /data/web_static/releases/{}".format(no_ext))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}"
            .format(file_name, no_ext))
        """Delete the archive"""
        run("rm /tmp/{}".format(file_name))
        """Move contents to host web_static"""
        run('mv /data/web_static/releases/{}/web_static/* \
/data/web_static/releases/{}/'.format(no_ext, no_ext))
        """Remove web_static dir"""
        run('rm -rf /data/web_static/releases/\
{}/web_static'.format(no_ext))
        """Delete the symbolic link"""
        run("rm -rf /data/web_static/current")
        """Create a new symbolic link"""
        run("ln -s /data/web_static/releases/{} /data/web_static/current"
            .format(no_ext))
        return True
    except Exception as e:
        return False
