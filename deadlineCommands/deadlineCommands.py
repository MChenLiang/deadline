#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time     : 2019/10/29 11:06
# @Email    : spirit_az@foxmail.com
# @Name     : deadlineCommands.py
__author__ = 'miaochenliang'

# import--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
import re
import os
import errno
import subprocess


def callDeadlineCommand(arguments, hideWindow=True):
    # On OSX, we look for the DEADLINE_PATH file. On other platforms, we use the environment variable.
    if os.path.exists("/Users/Shared/Thinkbox/DEADLINE_PATH"):
        with open("/Users/Shared/Thinkbox/DEADLINE_PATH") as f:
            deadlineBin = f.read().strip()
        deadlineCommand = deadlineBin + "/deadlinecommand"
    else:
        deadlineBin = os.environ['DEADLINE_PATH']
        if os.name == 'nt':
            deadlineCommand = deadlineBin + "\\deadlinecommand.exe"
        else:
            deadlineCommand = deadlineBin + "/deadlinecommand"

    startupinfo = None
    if hideWindow and os.name == 'nt':
        # Python 2.6 has subprocess.STARTF_USESHOWWINDOW,
        # and Python 2.7 has subprocess._subprocess.STARTF_USESHOWWINDOW,
        # so check for both.
        if hasattr(subprocess, '_subprocess') and hasattr(subprocess._subprocess, 'STARTF_USESHOWWINDOW'):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW
        elif hasattr(subprocess, 'STARTF_USESHOWWINDOW'):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    environment = {}
    for key in os.environ.keys():
        environment[key] = str(os.environ[key])

    # Need to set the PATH, cuz windows seems to load DLLs from the PATH earlier that cwd....
    if os.name == 'nt':
        environment['PATH'] = str(deadlineBin + os.pathsep + os.environ['PATH'])

    arguments.insert(0, deadlineCommand)
    output = ""
    attempts = 0
    while attempts < 10 and output == "":
        try:
            # Specifying PIPE for all handles to workaround a Python bug on Windows.
            # The unused handles are then closed immediatley afterwards.
            proc = subprocess.Popen(arguments, cwd=deadlineBin, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, startupinfo=startupinfo, env=environment)
            output, errors = proc.communicate()
        except (OSError, IOError) as e:
            if e.errno == errno.EINTR:
                attempts += 1
                if attempts == 10:
                    output = "ERROR: Failed to get results from Deadline Command 10 times."
                continue
            raise

    return output


def get_deadline_path():
    deadline_path = callDeadlineCommand(["-GetSettingsDirectory"]).replace('\\', '/')
    return deadline_path


# _____________________________________________ Deadline Temp
def get_deadline_temp_path():
    deadlineHome = callDeadlineCommand(["-GetCurrentUserHomeDirectory", ])
    deadlineHome = deadlineHome.replace("\n", "").replace("\r", "").replace('\\', '/')
    return deadlineHome + "/temp"


def get_deadline_version():
    ver_re = re.compile('[vV](\d+)')
    version_full = get_deadline_full_version()
    ver_match = ver_re.match(version_full)
    if ver_match:
        return int(ver_match.group(1))
    return 0


def get_deadline_full_version():
    version_full = callDeadlineCommand(['Version'])
    return version_full


# _____________________________________________ Pool & Group
def get_deadline_pools():
    output = callDeadlineCommand(["-pools", ])
    pools = output.splitlines()
    return pools


def get_deadline_groups():
    output = callDeadlineCommand(["-groups", ])
    groups = output.splitlines()
    return groups


# _____________________________________________ Task
def send_to_deadline(arg=list()):
    tempResults = callDeadlineCommand(arg)
    return tempResults


def job_status(cmd_info, job_id=list()):
    """
    使用命令改变任务状态
    :param cmd_info: deadline command 命令
    :param job_id: 任务id 列表
    :return:
    """
    if not job_id or not cmd_info:
        print (False)
        return False

    try:
        callDeadlineCommand([cmd_info, job_id])
        print (True)
        return True

    except Exception as e:
        print (e)
        return False


def suspend_job(job_id=list()):
    """
    暂停任务
    :param job_id: 任务id 列表
    :return: True or False
    """
    job_status('-SuspendJob', job_id)


def resume_job(job_id=list()):
    """
    恢复任务
    :param job_id: id列表
    :return: True or False
    """
    job_status('-ResumeJob', job_id)


def fail_job(job_id=list()):
    """
    失效任务
    :param job_id: id列表
    :return: True or False
    """
    job_status('-FailJob', job_id)


def resumeFail_job(job_id=list()):
    """
    恢复失效任务
    :param job_id: id列表
    :return: True or False
    """
    job_status('-ResumeFailedJob', job_id)
