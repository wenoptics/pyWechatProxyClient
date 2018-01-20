from pyWechatProxyClient.api.consts import TEXT, SYSTEM, SHARING, STICKER, PICTURE
from pyWechatProxyClient.api.model.Chat import Chat
from pyWechatProxyClient.api.model.Friend import Friend
from pyWechatProxyClient.api.model.Group import Group


class Message(object):
    def __init__(self):
        self._is_at = False
        self._url = ''
        self._member = None
        self._sender = None
        self._text = ''
        self._client = None
        self._type = None
        self._time = None

    def __str__(self):
        return 'Message<sender="{}",text="{}",time"{}">' \
            .format(self.sender, self.text, self._time)

    def set_message(self,
                    talker_id='',
                    time=None,
                    content='',
                    internal_type=-1
                    ):
        """
        Construct Wechat message
        :param internal_type:
        :param content:
        :param time:
        :param talker_id:
        :return:
        """

        if talker_id.endswith('@chatroom'):
            # This is a message from group chat
            sender_group = Group(group_chat_id=talker_id)
            self._sender = sender_group

            _split = content.split('\n')
            # Extract member
            member_id = _split[0]
            member_id = member_id[:-1]
            self._member = Chat(talker_id=member_id)

            if len(_split) > 1:
                content = '\n'.join(content.split('\n')[1:])
            else:
                content = ''

            # todo self._is_at

        else:
            # This is a message from a `friend`
            sender_friend = Friend(friend_id=talker_id)
            self._sender = sender_friend

        self._time = time

        # fixme I think these belong to somewhere else...
        from pyWechatProxyClient.serverApi import ServerApiConst, parse_url

        # Set message property according to content and the internal_type
        if internal_type == ServerApiConst.INTERNAL_TYPE_TEXT:
            self._type = TEXT
            self._text = content
        elif internal_type == ServerApiConst.INTERNAL_TYPE_SHARING:
            self._type = SHARING
            # parse xml and find the `url` field
            self._url = parse_url(content)
        elif internal_type == ServerApiConst.INTERNAL_TYPE_SYSTEM:
            self._type = SYSTEM
            self._text = content
        elif internal_type == ServerApiConst.INTERNAL_TYPE_STICKER:
            self._type = STICKER
            self._text = content
        elif internal_type == ServerApiConst.INTERNAL_TYPE_PHOTO:
            self._type = PICTURE
            self._text = content

        # elif todo more elif ...
        else:
            self._type = SHARING  # fixme
            self._text = content

    @property
    def type(self) -> str:
        """
        消息的类型
            消息的类型，目前可为以下值:
                # 文本
                TEXT = 'Text'
                # 位置
                MAP = 'Map'
                # 名片
                CARD = 'Card'
                # 提示
                NOTE = 'Note'
                # 分享
                SHARING = 'Sharing'
                # 图片
                PICTURE = 'Picture'
                # 语音
                RECORDING = 'Recording'
                # 文件
                ATTACHMENT = 'Attachment'
                # 视频
                VIDEO = 'Video'
                # 好友请求
                FRIENDS = 'Friends'
                # 系统
                SYSTEM = 'System'
        :return:
        """
        return self._type

    @property
    def is_at(self):
        """
        当为群消息时，返回时候被@
        :return:
        """
        raise NotImplementedError
        return self._is_at

    @property
    def sender(self) -> Chat:
        """
        消息的发送者 (群聊或是个人)
        :return:
        """
        return self._sender

    @sender.setter
    def sender(self, value):
        self._sender = value

    chat = sender

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        self._client = value
        self.sender.client = value

    @property
    def text(self):
        """
        消息的文本内容
        :return:
        """
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def url(self):
        """
        分享类消息中的网页 URL
        :return:
        """
        return self._url

    @property
    def member(self):
        """
        若消息来自群聊，则此属性为消息的实际发送人(具体的群成员)
        若消息来自其他聊天对象(非群聊)，则此属性为 None
        :return:
        """
        return self._member

    @property
    def create_time(self):
        """
        服务端发送时间
        """
        return self._time

    # --------------------------------
    # 回复方法

    def reply(self, *args, **kwargs):
        self.sender.send(*args, **kwargs)
