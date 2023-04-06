#!/usr/bin/env python3
"""
Fabric script that deletes out-of-date archives
"""

import os
from fabric.api import *

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'
env.key_filename = '/path/to/ssh/key'

def do_clean(number=0):
    """
    Deletes all unnecessary archives
    """
    number = int(number)
    if number < 1:
        number = 1

    with cd('/data/web_static/releases'):
        archives = sorted(run('ls -1tr').split('\n'))
        to_delete = archives[:-number]
        if len(to_delete) > 0:
            run('rm -f %s' % ' '.join(to_delete))

    with cd('/data/web_static/current'):
        archives = sorted(run('ls -1tr ../releases/').split('\n'))
        to_delete = archives[:-number]
        if len(to_delete) > 0:
            run('rm -f %s' % ' '.join(['../releases/' + x for x in to_delete]))

if __name__ == "__main__":
    do_clean(2)

