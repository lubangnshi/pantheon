import os
from os import path
import sys
import socket
import signal
import errno
import tempfile
import yaml
from datetime import datetime

import context
from subprocess_wrappers import check_call, call


def get_open_port():
    sock = socket.socket(socket.AF_INET)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return str(port)


def make_sure_dir_exists(d):
    try:
        os.makedirs(d)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

tmp_dir = path.join(tempfile.gettempdir(), 'pantheon-tmp')
make_sure_dir_exists(tmp_dir)

def parse_config():
    with open(path.join(context.src_dir, 'config.yml')) as config:
        return yaml.load(config)


def update_submodules():
    cmd = 'git submodule update --init --recursive'
    check_call(cmd, shell=True)


class TimeoutError(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutError()


def utc_time():
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


def kill_proc_group(proc, signum=signal.SIGTERM):
    if not proc:
        return

    try:
        sys.stderr.write('kill_proc_group: killed process group with pgid %s\n'
                         % os.getpgid(proc.pid))
        os.killpg(os.getpgid(proc.pid), signum)
    except OSError as exception:
        sys.stderr.write('kill_proc_group: %s\n' % exception)


def apply_patch(patch_name, repo_dir):
    patch = path.join(context.src_dir, 'wrappers', 'patches', patch_name)

    if call(['git', 'apply', patch], cwd=repo_dir) != 0:
        sys.stderr.write('patch apply failed but assuming things okay '
                         '(patch applied previously?)\n')
