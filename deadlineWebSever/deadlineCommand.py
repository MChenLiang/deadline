#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time     : 2019/11/26 14:54
# @Email    : spirit_az@foxmail.com
# @Name     : deadlineCommand.py
__author__ = 'miaochenliang'

# import--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
import gc
import subprocess
import sys
import os
import time
import tempfile

import editConf
import getAllSocket

_deadlineAPIPath = editConf.getAPIPath()
_deadlineAPIPath in sys.path or sys.path.append(_deadlineAPIPath)

try:
    from Deadline import DeadlineConnect
    from Deadline import ConnectionProperty
except ImportError:
    from ..Deadline import DeadlineConnect
    from ..Deadline import ConnectionProperty
except Exception as e:
    raise Exception("Import error : No Found deadline client")
else:
    print('initialize deadline success')


class deadlineCommand(object):
    _host = getAllSocket.getHostName()
    _port = editConf.getSeverAppPort()

    def __init__(self):
        self.appPath, self.appFolder, self.appName = editConf.getSeverApp()
        self._host = getAllSocket.getHostName()
        self._port = editConf.getSeverAppPort()
        self._app = None
        self.proc = None
        self._conn = None
        self.Jobs = None
        self.SlavesRenderingJob = None
        self.Tasks = None
        self.TaskReports = None
        self.JobReports = None
        self.LimitGroups = None
        self.Pulse = None
        self.Repository = None
        self.MappedPaths = None
        self.MaximumPriority = None
        self.Pools = None
        self.Groups = None
        self.Plugins = None
        self.Slaves = None
        self.Users = None
        self.Balancer = None

    def startSever(self):
        self._startSever()

        self._app = getAllSocket.appIsOpen(self.appName)
        self._conn = DeadlineConnect.DeadlineCon(self._host, self._port)
        self.Jobs = self._conn.Jobs
        self.SlavesRenderingJob = self._conn.SlavesRenderingJob
        self.Tasks = self._conn.Tasks
        self.TaskReports = self._conn.TaskReports
        self.JobReports = self._conn.JobReports
        self.LimitGroups = self._conn.LimitGroups
        self.Pulse = self._conn.Pulse
        self.Repository = self._conn.Repository
        self.MappedPaths = self._conn.MappedPaths
        self.MaximumPriority = self._conn.MaximumPriority
        self.Pools = self._conn.Pools
        self.Groups = self._conn.Groups
        self.Plugins = self._conn.Plugins
        self.Slaves = self._conn.Slaves
        self.Users = self._conn.Users
        self.Balancer = self._conn.Balancer

    def _closeSever(self):
        """
        关闭服务,这只是一个测试。
        :return:
        """
        getAllSocket.killProcessByPid(self._app.pid)
        conn = getAllSocket.checkPort(self._port)
        while conn:
            time.sleep(0.2)
            conn = getAllSocket.checkPort(self._port)
        del self._conn
        del self._app
        del self.proc

        gc.collect()

    def _startSever(self):
        app = getAllSocket.appIsOpen(self.appName)
        if app:
            return
        tmp_file = os.path.normcase(os.path.join(os.path.dirname(tempfile.mktemp()), 'startDeadlineWebSever.bat'))
        with open(tmp_file, 'w') as f:
            f.write('''
@echo off
if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("%~nx0 h",0)(window.close)&&exit
:begin\n''')
            f.write('"{}"\n'.format(self.appPath))
            f.write('pause')

        proc = subprocess.Popen('explorer.exe "{0}"'.format(tmp_file))
        del proc
        gc.collect()

        conn = getAllSocket.checkPort(self._port)
        while not conn:
            time.sleep(0.2)
            conn = getAllSocket.checkPort(self._port)


if __name__ == '__main__':
    p = deadlineCommand()
    p.startSever()
    print p.Groups.GetGroupNames()
