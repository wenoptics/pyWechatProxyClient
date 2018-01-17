class Chat:
    def __init__(self, talker_id=''):
        # talker_id是对方的id
        self.talker_id = talker_id
        self.username = ''
        self.client = None

    def set_client(self, v):
        self.client = v

    def __str__(self):
        return 'Chat<talker_id="{}">'.format(self.talker_id)

    def send(self, content, *args, **kwargs):
        if self.client is None:
            raise ValueError('No client bind to this chat yet.')

        from pyWechatProxyClient.api.model.Message import Message

        if not isinstance(content, Message):
            msg = Message()
            msg.sender = self
            msg.text = content
            self.client.send_message_queue.put(msg)
        else:
            self.client.send_message_queue.put(content)

    def __eq__(self, other: 'Chat'):
        return self.talker_id == other.talker_id
