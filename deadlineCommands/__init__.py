#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time     : 2019/11/12 14:44
# @Email    : spirit_az@foxmail.com
# @Name     : __init__.py.py
__author__ = 'miaochenliang'

# import--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
__all__ = ['getFirstPool', 'getSecondPool', 'getDeadlineVersion']
from . import editConf, deadlineCommands


def getFirstPool(keyword=''):
    return editConf.getFirstPool(keyword)


def getSecondPool(keyword=''):
    return editConf.getSecondPool(keyword)


def getDeadlineVersion():
    return editConf.getDeadlineVersion()


def getDeadlineTmp():
    return deadlineCommands.get_deadline_temp_path()


def send_to_deadline(arguments):
    """

    :param arguments:  list()
    :return:
    """
    return deadlineCommands.callDeadlineCommand(arguments)

# def getHType():
#     return editConf.getSupportNodeType()
