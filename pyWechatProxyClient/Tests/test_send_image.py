import logging
import unittest

import time

from pyWechatProxyClient.Client import Client
from pyWechatProxyClient.api.consts import PICTURE
from pyWechatProxyClient.api.model.Message import Message
from pyWechatProxyClient.api.model.Friend import Friend

logging.basicConfig(level=logging.DEBUG)


class MyTestCase(unittest.TestCase):
    url = 'ws://192.168.1.161:5000/wechat'
    client = Client(url)

    def test_something(self):
        wen = Friend(friend_id='wenoptics')
        wen.client = self.client

        @self.client.register(wen)
        def on_message(msg: Message):
            print('on wen\'s message! {}'.format(msg))

            if msg.text == '#stop':
                print("stop called")
                self.client.stop()
                return

            return 'cool!'

        self.client.start()

        time.sleep(1)
        
        img_list = [
            './dataset/dae7d170bb63b2951589ab45d96aaf2a.png',
            './dataset/2.png'
        ]
        for i in img_list:
            img_msg = Message(PICTURE)
            img_msg.text = i
            wen.send(img_msg)

        self.client.join()



if __name__ == '__main__':
    unittest.main()
