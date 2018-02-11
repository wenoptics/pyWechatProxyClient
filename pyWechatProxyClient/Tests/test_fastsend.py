import logging
import unittest

import time

from pyWechatProxyClient.Client import Client
from pyWechatProxyClient.api.model.Friend import Friend

logging.basicConfig(level=logging.DEBUG)


class MyTestCase(unittest.TestCase):

    url = 'ws://192.168.1.161:5000/wechat'
    client = Client(url)

    def test_something(self):
        wen = Friend(friend_id='wenoptics')
        wen.client = self.client

        self.client.start()

        wen.send("bla-bup")
        wen.send("bla-bup1")
        wen.send("bla-bup2")
        wen.send("bla-bup3")
        wen.send("bla-bup4")
        wen.send("bla-bup5")

        time.sleep(5)


if __name__ == '__main__':
    unittest.main()
