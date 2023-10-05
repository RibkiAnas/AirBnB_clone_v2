#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive
from the contents of the web_static folder
"""
from fabric.api import local
from time import strftime
from datetime import datetime


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
