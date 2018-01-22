from unittest import TestCase

from pyWechatProxyClient.serverApi import parse_time


class TestParse_time(TestCase):
    def test_parse_time(self):
        s = '1515919449000'
        t = parse_time(s)
        print(t)
