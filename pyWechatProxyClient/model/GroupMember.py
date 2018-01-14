from pyWechatProxyClient.model import Group


class GroupMember:
    def __init__(self):
        self._display_name = None
        self.__belong_group = None

    @property
    def display_name(self):
        """
        在群聊中的显示昵称
        :return:
        """
        return self._display_name

    @property
    def name(self):
        """
        该群成员的友好名称
            具体为: 从 群聊显示名称、昵称(或群名称)，或微信号中，按序选取第一个可用的
        :return:
        """
        return # todo
