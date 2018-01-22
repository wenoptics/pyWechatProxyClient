import logging
from unittest import TestCase

from pyWechatProxyClient.backend.WebSocketClientEngine import WebSocketClientEngine, logger


class TestWebSocketClientEngine(TestCase):
    def test_engine(self):

        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)

        url = 'ws://192.168.1.161:5000/wechat'
        engine = WebSocketClientEngine(url)
        print("now you should send some message to this engine client")
        engine.start_listen()

        while True:
            pass