#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time     : 2019/11/12 14:57
# @Email    : spirit_az@foxmail.com
# @Name     : editConf.py
__author__ = 'miaochenliang'

# import--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
import platform
import re
import json

pyVersion = platform.python_version()
totalPyVer = int(pyVersion[0])
if totalPyVer > 2:
    import configParser as ConfigParser
else:
    import ConfigParser

import os
import deadlineConfEnv as env

# proc  --+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
_absPath_ = os.path.dirname(__file__)


# function   +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
class _conf(object):
    @property
    def INIPATH(self):
        return self._in_path

    @INIPATH.setter
    def INIPATH(self, val):
        self._in_path = val

    @INIPATH.deleter
    def INIPATH(self):
        self._in_path = os.path.join(_absPath_, 'deadlineConf.ini').replace('\\', '/')

    def __init__(self):
        self.cf = ConfigParser.ConfigParser()
        self._in_path = os.path.join(_absPath_, 'deadlineConf.ini').replace('\\', '/')

    def init_conf(self):
        self.cf.read(self.INIPATH)

    def get(self, field, key):
        try:
            self.cf.read(self.INIPATH)
            result = self.cf.get(field, key)
        except:
            result = ""

        return result

    def set(self, field, key, val):
        if self.find(field, key):
            self.cf.remove_option(field, key)
        if not self.has_section(field):
            self.cf.add_section(field)
        self.cf.set(field, key, val)
        self._write()

    def has_section(self, section):
        self.cf.read(self.INIPATH)
        return self.cf.has_section(section)

    def delete_section(self, field):
        section = self.has_section(field)
        section and self.cf.remove_section(section)
        self._write()

    def delete_op(self, field, key):
        if self.find(field, key):
            self.cf.remove_option(field, key)
        self._write()

    def find(self, field, key):
        self.cf.read(self.INIPATH)
        return self.cf.has_option(field, key)

    def _write(self):
        with open(self._in_path, 'wb') as f:
            self.cf.write(f)


def reloadDeadlineConf():
    """

    DEADLINE_MESSAGE = "DEADLINE_MESSAGE"
    DEADLINE_SEVER_PATH = "serve_app_path"
    DEADLINE_SEVER_APP = "sever_app_name"
    DEADLINE_SEVER_PORT = "sever_con_port"

    :return:
    """
    conf = _conf()
    conf.init_conf()

    DEADLINE_MESSAGE = env.DEADLINE_MESSAGE
    DEADLINE_SEVER_PATH = env.DEADLINE_SEVER_PATH
    DEADLINE_SEVER_APP = env.DEADLINE_SEVER_APP
    DEADLINE_SEVER_PORT = env.DEADLINE_SEVER_PORT
    DEADLINE_API_PATH = env.DEADLINE_API_PATH

    deadlineSeverPath, deadlineBin, deadlineSever = getSeverApp()

    conf.set(DEADLINE_MESSAGE, DEADLINE_SEVER_PATH, deadlineBin)
    conf.set(DEADLINE_MESSAGE, DEADLINE_SEVER_APP, deadlineSever)
    # deadline port, wo can open deadlineWebSever.exe to get it
    conf.set(DEADLINE_MESSAGE, DEADLINE_SEVER_PORT, 8082)
    conf.set(DEADLINE_MESSAGE, DEADLINE_API_PATH, u'you deadline serve path /api/python')


def get(field, key):
    conf = _conf()
    conf.init_conf()
    return conf.get(field, key)


def getSeverAppPath():
    return get(env.DEADLINE_MESSAGE, env.DEADLINE_SEVER_PATH)
    pass


def getSeverAppName():
    return get(env.DEADLINE_MESSAGE, env.DEADLINE_SEVER_APP)
    pass


def getSeverApp():
    if os.path.exists("/Users/Shared/Thinkbox/DEADLINE_PATH"):
        with open("/Users/Shared/Thinkbox/DEADLINE_PATH") as f:
            deadlineBin = f.read().strip()
        deadlineCommand = "deadlinewebservice"
    else:
        deadlineBin = os.environ['DEADLINE_PATH']
        if os.name == 'nt':
            deadlineCommand = "deadlinewebservice.exe"
        else:
            deadlineCommand = "deadlinewebservice"
    return os.path.join(deadlineBin, deadlineCommand).replace('\\', '/'), deadlineBin, deadlineCommand


def getSeverAppPort():
    return int(get(env.DEADLINE_MESSAGE, env.DEADLINE_SEVER_PORT))


def getAPIPath():
    return get(env.DEADLINE_MESSAGE, env.DEADLINE_API_PATH)


if __name__ == "__main__":
    reloadDeadlineConf()
