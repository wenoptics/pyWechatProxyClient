
class Client:
    def __init__(self):
        pass

    @property
    def friends(self):
        """
        获取所有好友
        :return:
        """
        return []

    @property
    def groups(self):
        """
        获取所有群聊对象
        :return: 群聊合集
        """
        return []

    @property
    def chats(self):
        """
        获取所有聊天对象
        :return: 聊天对象合集
        """
        return []

    def start(self):
        """
        开始消息监听和处理
        :return:
        """
        pass

    def stop(self):
        """
        停止消息监听和处理
        :return:
        """
        pass

    def join(self):
        """
        堵塞收消息进程
        :return:
        """
        pass