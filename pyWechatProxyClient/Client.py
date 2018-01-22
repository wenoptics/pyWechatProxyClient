import logging
import queue
import threading

import time

from pyWechatProxyClient.api.consts import SYSTEM
from pyWechatProxyClient.serverApi import parse_message, make_message
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
        self.is_running = False
        self.listening_thread = None
        self.sending_thread = None
        self.__stop_evt = threading.Event()
        self.ws_engine = WebSocketClientEngine(self.server_url)
        self.send_message_queue = queue.Queue()
        self.__system_message_handler = None

    def __str__(self):
        return '<WechatProxyClient "{}">'.format(self.server_url)

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

    def set_system_message_handler(self, handler):
        """
        收到系统消息的callback
        :param handler: 原型：
            yourCallback(client: Client, message: Message)
        :return:
        """
        import inspect
        if not inspect.isfunction(handler):
            raise ValueError('handler is not function')
        self.__system_message_handler = handler

    def start(self):
        """
        开始消息监听和处理
        :return:
        """
        self.is_running = True
        if self.listening_thread:
            logger.warning('{} is already running, no need to start again.'.format(self))
        else:
            self.listening_thread = start_new_thread(self._listen)
        if not self.sending_thread:
            self.sending_thread = start_new_thread(self._send)

    def stop(self):
        """
        停止消息监听和处理
        :return:
        """
        self.is_running = False
        self.__stop_evt.set()
        self.ws_engine.stop()
        self.join()

    def join(self):
        """
        堵塞收发消息进程
        :return:
        """
        if self.listening_thread:
            self.listening_thread.join()
        if self.sending_thread:
            self.sending_thread.join()

    def _send(self):
        """
        Constantly checking the sendQueue and send message if have one
        :return:
        """
        try:
            logger.info('{}: sending-queue checking started.'.format(self))
            while not self.__stop_evt.is_set():
                try:
                    # Specify a timeout so that there is a chance for this thread to check `.is_running`
                    #       otherwise it won't respond to the `.stop()` call
                    msg = self.send_message_queue.get(timeout=1)
                except queue.Empty:
                    continue
                if msg is None:
                    continue
                try:
                    str_msg = make_message(msg)
                except Exception as e:
                    logger.error('Make message failed:', e)
                from websocket._exceptions import WebSocketConnectionClosedException
                while str_msg:
                    # Wait socket loop
                    try:
                        self.ws_engine.send(str_msg)
                        break
                    except WebSocketConnectionClosedException:
                        time.sleep(1)
                        logger.debug('retry sending message...')
                        continue
                    except Exception as e:
                        logger.error('send message failed', e)
                        break
                # Still in _send main loop

        finally:
            self.sending_thread = None
            logger.info('{}: stopped send-queue checking.'.format(self))

    def _listen(self):
        try:
            logger.info('{}: started listen wechat messages'.format(self))

            def _on_message(msg):
                wechat_message = parse_message(msg)
                if wechat_message:
                    self._process_message(wechat_message)

            self.ws_engine.add_message_handler(_on_message)

            # fixme ----- For debug usage -----
            from pyWechatProxyClient.backend.WebSocketClientEngine import logger as engine_logger
            engine_logger.addHandler(logging.StreamHandler())
            engine_logger.setLevel(logging.DEBUG)

            self.ws_engine.start_listen()

        finally:
            self.listening_thread = None
            logger.info('{}: stopped listen wechat messages'.format(self))

    def _process_message(self, msg: Message):
        """
        处理接收到的消息
        """
        msg.client = self

        # On system message:
        if msg.type == SYSTEM:
            if self.__system_message_handler is not None:
                self.__system_message_handler(self, msg)

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

