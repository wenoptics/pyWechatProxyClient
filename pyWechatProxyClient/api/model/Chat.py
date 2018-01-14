from pyWechatProxyClient.api.model import Message


class Chat:
    def __init__(self, talker_id=''):
        # talker_id是对方的id
        self.talker_id = talker_id
        self.username = ''

    def __str__(self):
        return 'Chat<talker_id="{}">'.format(self.talker_id)

    def send(self, content: Message =None):
        #todo
        pass

    def __eq__(self, other: 'Chat'):
        return self.talker_id == other.talker_id
