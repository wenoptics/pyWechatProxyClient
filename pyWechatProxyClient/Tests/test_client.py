from unittest import TestCase
import logging

from pyWechatProxyClient.Client import Client, logger as cLogger
from pyWechatProxyClient.api.model.Friend import Friend
from pyWechatProxyClient.api.model.Message import Message


class TestClient(TestCase):
    url = 'ws://192.168.1.161:5000/wechat'
    client = Client(url)

    def test_handle_message(self):

        cLogger.addHandler(logging.StreamHandler())
        cLogger.setLevel(logging.DEBUG)

        wen = Friend(friend_id='wenoptics')

        @self.client.register(wen)
        def on_message(msg: Message):
            print('on wen\'s message! {}'.format(msg))

            if msg.text == '#stop':
                print("stop called")
                self.client.stop()
                return

            # return 'cool!'

        self.client.start()
        self.client.join()

    def test__listen(self):
        return
        self.client.start()
        self.client.join()
