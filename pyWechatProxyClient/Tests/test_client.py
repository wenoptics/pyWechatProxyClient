from unittest import TestCase

from pyWechatProxyClient.Client import Client
from pyWechatProxyClient.api.model.Friend import Friend
from pyWechatProxyClient.api.model.Message import Message


class TestClient(TestCase):
    url = 'ws://192.168.1.161:5000/wechat'
    client = Client(url)

    def test_handle_message(self):

        wen = Friend(friend_id='wenoptics')

        @self.client.register(wen)
        def on_message(msg: Message):
            print('on wen\'s message! {}'.format(msg))

        self.client.start()
        self.client.join()

    def test__listen(self):
        return
        self.client.start()
        self.client.join()
