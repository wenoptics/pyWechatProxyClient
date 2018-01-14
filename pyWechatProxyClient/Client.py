import asyncio
import logging

from pyWechatProxyClient.ServerApi import parse_message
from pyWechatProxyClient.api.message.message_config import MessageConfig
from pyWechatProxyClient.api.message.registered import Registered
from pyWechatProxyClient.api.model.Message import Message
from pyWechatProxyClient.backend.WebSocketClientEngine import WebSocketClientEngine
from pyWechatProxyClient.utils.util import start_new_thread

logger = logging.getLogger(__name__)


class Client:
    def __init__(self, wx_proxy_server_url):

        self.server_url = wx_proxy_server_url
        self.registered = Registered(self)
        self.is_listening = False
        self.listening_thread = None

    @property
    def friends(self):
        """
        获取所有好友
        :return:
        """
        return []

    @property
    def groups(self):
        """
        获取所有群聊对象
        :return: 群聊合集
        """
        return []

    @property
    def chats(self):
        """
        获取所有聊天对象
        :return: 聊天对象合集
        """
        return []

    def register(
            self, chats=None, msg_types=None,
            run_async=True, enabled=True
    ):
        """
        装饰器：用于注册消息配置

        :param chats: 消息所在的聊天对象：单个或列表形式的多个聊天对象或聊天类型，为空时匹配所有聊天对象
        :param msg_types: 消息的类型：单个或列表形式的多个消息类型，为空时匹配所有消息类型 (SYSTEM 类消息除外)
        :param run_async: 是否异步执行所配置的函数：可提高响应速度
        :param enabled: 当前配置的默认开启状态，可事后动态开启或关闭
        """

        def do_register(func):
            self.registered.append(MessageConfig(
                client=self, func=func, chats=chats, msg_types=msg_types,
                run_async=run_async, enabled=enabled
            ))

            return func

        return do_register

    def start(self):
        """
        开始消息监听和处理
        :return:
        """
        if self.is_listening:
            logger.warning('{} is already running, no need to start again.'.format(self))
        else:
            self.listening_thread = start_new_thread(self._listen)

    def stop(self):
        """
        停止消息监听和处理
        :return:
        """
        # todo
        pass

    def join(self):
        """
        堵塞收消息进程
        :return:
        """
        if (self.listening_thread):
            self.listening_thread.join()

    def _listen(self):
        try:
            self.is_listening = True
            logger.info('{}: started listen'.format(self))

            asyncio.set_event_loop(loop)
            WebSocketClientEngine.set_server_url(self.server_url)
            ws_engine = WebSocketClientEngine(event_loop=loop)

            # fixme For debug usage
            ws_engine.logger.addHandler(logging.StreamHandler())
            ws_engine.logger.setLevel(logging.DEBUG)

            async def _receive():
                while True:
                    message = await ws_engine.messageQueue.get()
                    wechat_message = parse_message(message)
                    #print(wechat_message)
                    if wechat_message:
                        self._process_message(wechat_message)

            # blocked here
            loop.run_until_complete(
                asyncio.wait([ws_engine.run(), _receive()])
            )

        finally:
            self.is_listening = False
            logger.info('{}: stopped listen'.format(self))

    def _process_message(self, msg: Message):
        """
        处理接收到的消息
        """

        config = self.registered.get_config(msg)

        logger.debug('{}: new message (func: {}):\n{}'.format(
            self, config.func.__name__ if config else None, msg))

        if config:

            def process():
                # noinspection PyBroadException
                try:
                    ret = config.func(msg)
                    if ret is not None:
                        msg.reply(ret)
                except:
                    logger.exception('an error occurred in {}.'.format(config.func))

                    # 标记已读
                    # if self.auto_mark_as_read and not msg.type == SYSTEM and msg.sender != self.self:
                    #     from wxpy import ResponseError
                    #     try:
                    #         msg.chat.mark_as_read()
                    #     except ResponseError as e:
                    #         logger.warning('failed to mark as read: {}'.format(e))

            if config.run_async:
                start_new_thread(process, use_caller_name=True)
            else:
                process()

loop = asyncio.get_event_loop()