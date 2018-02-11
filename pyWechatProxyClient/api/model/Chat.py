import logging

logger = logging.getLogger(__name__)


class Chat:
    def __init__(self, talker_id='', nickname=None):
        # talker_id是对方的id
        self.talker_id = talker_id
        username = talker_id
        self.client = None
        # Wechat nickname
        self.name = nickname if nickname else talker_id
        if not talker_id:
            logger.warning('talker_id="%s", may not be valid', talker_id)

    def set_client(self, v):
        self.client = v

    def __str__(self):
        return '<{} name="{}", talker_id="{}">'.format(self.__class__.__name__, self.name, self.talker_id)

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
