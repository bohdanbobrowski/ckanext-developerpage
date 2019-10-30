from datetime import datetime
import json
import inspect
import logging
import os
from ckan.common import config, is_flask_request, c, request
from ckan.plugins import toolkit
from ckan.logic.action.get import status_show
import ckan.model as model
from ckan.common import g, config, _
import platform
import humanize as hz
from uptime import boottime

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
            'uptime': boottime(),
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
