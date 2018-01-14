from pyWechatProxyClient.Client import Client
from pyWechatProxyClient.model.Chat import Chat


class Message:
    def __init__(self):
        self._text = None
        self._client = None
        self._type = None

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
    def sender(self) -> Chat:
        """
        消息的发送者 (群聊或是个人)
        :return:
        """
        pass

    @property
    def client(self) -> Client:
        return self._client

    @property
    def text(self):
        """
        消息的文本内容
        :return:
        """
        return self._text

    @property
    def url(self):
        """
        分享类消息中的网页 URL
        :return:
        """
        pass

    @property
    def member(self):
        """
        若消息来自群聊，则此属性为消息的实际发送人(具体的群成员)
        若消息来自其他聊天对象(非群聊)，则此属性为 None
        :return:
        """
        pass

    #--------------------------------
    # 回复方法

    def reply(self, *args, **kwargs):
        self.sender.send(*args, **kwargs)
