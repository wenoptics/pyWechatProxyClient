import logging
from unittest import TestCase

from pyWechatProxyClient.backend.WebSocketClientEngine import WebSocketClientEngine


class TestWebSocketClientEngine(TestCase):
    def test_engine(self):
        engine = WebSocketClientEngine()
        engine.logger.addHandler(logging.StreamHandler())
        engine.logger.setLevel(logging.DEBUG)
        print("now you should send some message to this engine client")
        engine.start()
