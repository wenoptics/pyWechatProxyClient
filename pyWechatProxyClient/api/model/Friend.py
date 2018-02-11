from pyWechatProxyClient.api.model.Chat import Chat


class Friend(Chat):
    def __init__(self, friend_id='', nickname=None):
        super().__init__(talker_id=friend_id, nickname=nickname)

