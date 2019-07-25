from datetime import datetime
import json
import inspect
import logging
import os

from ckan.common import config, is_flask_request, c, request
from ckan.plugins import toolkit
from ckan.logic.action.get import status_show

import ckan.model as model
import ckan.logic as logic

from ckan.common import g, config, _

import platform
import humanize as hz
import subprocess


log = logging.getLogger(__name__)


def humanize(value):
    return hz.naturalsize(value, gnu=True)


def memory_info():
    import psutil
    memory = psutil.virtual_memory()
    cpu_times = psutil.cpu_times_percent()
    return {
            'memory_available' : humanize(memory.available),
            'memory_used' : str(memory.percent) + "%",
            'cpu_user_mode' : str(cpu_times.user) + "%",
            'cpu_kernel_mode' : str(cpu_times.system) + "%",
            'cpu_idle' : str(cpu_times.idle) + '%',
        }


def load_average_5min():
    import psutil
    return {
            'load_average_5min' : '{:.2f}'.format(psutil.getloadavg()[1]),
        }

def get_host_info():
    python_platform = {
            'machine_architecture' : platform.machine(),
            'python_version' : platform.python_version(),
        }
    memory = memory_info()
    load = load_average_5min()
    python_platform.update(memory)
    python_platform.update(load)
    return python_platform

def get_ckan_info():
    context = {
            u'model': model,
            u'user': g.user,
            u'auth_user_obj': g.userobj}
    return status_show(context, data_dict={})

def get_git_branch():
    '''Return git describe result'''
    branches = subprocess.check_output(["git", "branch"]).strip()
    branches = branches.split('\n')
    for branch in branches:
        if branch.find('* ') == 0:
            return branch
    return ''

def get_git_describe():
    '''Return git describe result'''
    return subprocess.check_output(["git", "describe"]).strip()

def get_git_head():
    '''Return last commit hash'''
    return subprocess.check_output(["git", "rev-parse", "--verify", "HEAD"]).strip()
