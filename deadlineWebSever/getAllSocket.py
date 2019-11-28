#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time     : 2019/11/22 10:19
# @Email    : spirit_az@foxmail.com
# @Name     : getAllSocket.py
__author__ = 'miaochenliang'

# import--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
import os
import re
import socket
import psutil
import sys
from subprocess import check_output


def getIpAddrs():
    # 得到所有的host
    return socket.getaddrinfo(socket.gethostname(), None)


def getHostName():
    host = socket.gethostname()
    return socket.gethostbyname(host)


def getActiveNetStat():
    ret = os.popen("netstat -ano")
    strList = ret.read().decode('gb2312').split('\n')
    for each in strList[4:]:
        yield re.split(' +', each)[1:]


def getAppAddrs(pid):
    for each in getAllConns():
        if each.pid == pid:
            return each
    return False


def getAllConns():
    """
    # 'sconn', ['fd', 'family', 'type', 'laddr', 'raddr', 'status', 'pid']
    # type {1: "TCP", 2: "UDP"}
    :return:
    """
    return psutil.net_connections()


def open_text(fname, **kwargs):
    """On Python 3 opens a file in text mode by using fs encoding and
    a proper en/decoding errors handler.
    On Python 2 this is just an alias for open(name, 'rt').
    """
    PY3 = sys.version_info[0] == 3
    if PY3:
        # See:
        # https://github.com/giampaolo/psutil/issues/675
        # https://github.com/giampaolo/psutil/pull/733
        FS_ENCODING = sys.getfilesystemencoding()
        ENCODING_ERRORS_HANDLER = 'surrogateescape'
        kwargs.setdefault('encoding', FS_ENCODING)
        kwargs.setdefault('errors', ENCODING_ERRORS_HANDLER)
    return open(fname, "rt", **kwargs)


def getAllProcess():
    """
    psutil.Process(pid=9516, name='ZBrush.exe')
    :return:
    """
    return psutil.process_iter()


def appIsOpen(appName):
    """
    从所有开着的app中筛选出来
    :param appName:
    :return:
    """
    for each in getAllProcess():
        if each.name() == appName:
            return each
    return False


def checkPort(port):
    for each in getAllConns():
        if each.laddr[1] == port:
            return each
    return False


def killProcessByPort(port):
    p = checkPort(port)
    if p:
        killProcessByPid(p.pid)


def killProcessByPid(pid):
    try:
        os.popen('taskkill /pid ' + str(pid) + ' /F ')
    except:
        pass
