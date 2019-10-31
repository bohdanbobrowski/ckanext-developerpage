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
import os
import platform

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

def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

def get_host_info():
    python_platform = {
            'machine_architecture' : platform.machine(),
            'python_version' : platform.python_version(),
            'uptime': datetime.utcfromtimestamp(creation_date('/srv/app/production.ini')).strftime('%Y-%m-%d %H:%M:%S'),
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
