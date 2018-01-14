from pyWechatProxyClient.api.model.Chat import Chat


class Friend(Chat):
    def __init__(self, friend_id=''):
        super().__init__(talker_id=friend_id)

