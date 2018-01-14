from pyWechatProxyClient.model import Message


class Chat:
    def __init__(self, talker_id=''):
        # talker_id是对方的id
        self.talker_id = talker_id
        self.username = ''

    def send(self, content: Message=None):
        #todo
        pass

    