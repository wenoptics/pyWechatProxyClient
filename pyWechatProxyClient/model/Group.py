from pyWechatProxyClient.model.Chat import Chat


class Group(Chat):
    def __init__(self, group_chat_id=''):
        super().__init__(chat_id=group_chat_id)
        self._is_owner = None

    @property
    def is_owner(self):
        """
        是否是群主
        :return:
        """
        return self._is_owner
