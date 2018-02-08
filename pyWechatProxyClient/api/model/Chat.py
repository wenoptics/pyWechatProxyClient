class Chat:
    def __init__(self, talker_id=''):
        # talker_id是对方的id
        self.talker_id = talker_id
        self.username = ''
        self.client = None
        self.name = talker_id  # todo This is no supported by WechatProxy yet... use _id now

    def set_client(self, v):
        self.client = v

    def __str__(self):
        return '{}<talker_id="{}">'.format(self.__class__.__name__, self.talker_id)

    def __repr__(self):
        return self.__str__()

    def send(self, content, *args, **kwargs):
        if self.client is None:
            raise ValueError('No client bind to this chat yet.')

        if not content:
            return

        from pyWechatProxyClient.api.model.Message import Message

        if not isinstance(content, Message):
            msg = Message()
            msg.sender = self
            msg.text = content
            self.client.send_message_queue.put(msg)
        else:
            self.client.send_message_queue.put(str(content))

    def __eq__(self, other: 'Chat'):
        return self.talker_id == other.talker_id
