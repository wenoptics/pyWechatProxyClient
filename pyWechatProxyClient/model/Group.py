from pyWechatProxyClient.model.Chat import Chat


class Group(Chat):
    def __init__(self):
        super().__init__()
        self._is_owner = None

    @property
    def is_owner(self):
        """
        是否是群主
        :return:
        """
        return self._is_owner
