from pyWechatProxyClient.api.model.Chat import Chat


class Group(Chat):
    def __init__(self, group_chat_id='', groupname=None):
        super().__init__(talker_id=group_chat_id, nickname=groupname)
        self._is_owner = None  # todo Not supported yet

    @property
    def is_owner(self):
        """
        是否是群主
        :return:
        """
        return self._is_owner
