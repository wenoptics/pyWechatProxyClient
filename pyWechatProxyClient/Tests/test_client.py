from unittest import TestCase

from pyWechatProxyClient.Client import Client


class TestClient(TestCase):
    def test__listen(self):
        client = Client()
        client.start()
        client.join()
