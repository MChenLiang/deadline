# deadline
Deadline connection development template

使用之前，我们需要根据我们的deadline配置，来重新定制".ini"的配置信息。
重新定制：
    对应editConf下的reloadDeadlineConf方法。

# deadlineCommands
    后台调用deadlinecommand.exe来实现操作。


# deadlineWebSever
    后台启动deadlinewebservice.exe， 使用deadlineAPI来实现操作。


example:
# 导入库
from deadline.deadlineWebSever import deadlineCommand
# 实例连接
deadlineCommand = deadlineCommand.deadlineCommand()
# 启动服务 ： 如果没有启动的话，会自动启动socket服务
deadlineCommand.startSever()
# 使用案例： 得到所有的组信息
deadlineCommand.Groups.GetGroupNames()
