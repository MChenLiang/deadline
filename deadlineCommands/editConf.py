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
import deadlineCommands as dCmds

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
    messageField = env.DEADLINE_BASE_FIELD
    ver = env.DEADLINE_VERSION
    fp = env.DEADLINE_PATH
    # support = env.DEADLINE_SUPPORT_NODE

    field = env.DEADLINE_POOL_FIELD
    firstPool = env.FIRST_POOL
    secondPool = env.SECOND_POOL
    # nodeType = env.HOUDINI_NODE_TYPE

    # 指针
    conf = _conf()
    conf.init_conf()

    deadlineVer = dCmds.get_deadline_full_version()
    deadlinePath = ""  # dCmds.get_deadline_path()
    conf.set(messageField, ver, deadlineVer)
    conf.set(messageField, fp, deadlinePath)

    allPool = dCmds.get_deadline_pools()
    conf.set(field, firstPool, allPool)
    conf.set(field, secondPool, allPool)


def _getPool(key, keyword=''):
    conf = _conf()
    conf.init_conf()
    allPool = eval(conf.get(env.DEADLINE_POOL_FIELD, key))
    if keyword:
        allPool = [each for each in allPool if re.search(keyword, each)]
    return allPool


def _getMessage(key):
    conf = _conf()
    conf.init_conf()
    Message = conf.get(env.DEADLINE_BASE_FIELD, key)
    return Message


def getFirstPool(keyword=''):
    return _getPool(env.FIRST_POOL, keyword)


def getSecondPool(keyword=''):
    return _getPool(env.SECOND_POOL, keyword)


def getDeadlineVersion():
    fullVer = _getMessage(env.DEADLINE_VERSION)
    return fullVer.split(' ')[0]
