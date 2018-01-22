from unittest import TestCase

from pyWechatProxyClient.serverApi import parse_url

xml_str = \
"""
<?xml version="1.0"?>
<msg>
<appmsg appid="" sdkver="0">
    <title>点击该链接添加为《部落冲突:皇室战争》好友！</title>
    <des>在《部落冲突:皇室战争》中打开链接或下载游戏。</des>
    <action>view</action>
    <type>5</type>
    <showtype>0</showtype>
    <content />
    <url>https://link.clashroyale.com/invite/friend/cn?tag=8YVGLC8C&amp;token=3kk7dc7h&amp;platform=iOS</url>
    <dataurl />
    <lowurl />
    <lowdataurl />
    <recorditem><![CDATA[]]></recorditem>
    <thumburl />
    <extinfo />
    <sourceusername />
    <sourcedisplayname />
    <commenturl />
    <appattach>
        <totallen>0</totallen>
        <attachid />
        <emoticonmd5 />
        <fileext />
        <cdnthumburl>304a0201000443304102010002049d7fc24802032f57260204a7c1346e02045a572ecf041c77656e6f7074696373315f6d73655f313531353636333035343135380204010800050201000400</cdnthumburl>
        <cdnthumblength>31472</cdnthumblength>
        <cdnthumbheight>340</cdnthumbheight>
        <cdnthumbwidth>340</cdnthumbwidth>
        <aeskey>49c8758d8366f03fa6b0a37c92692204</aeskey>
        <cdnthumbaeskey>49c8758d8366f03fa6b0a37c92692204</cdnthumbaeskey>
    </appattach>
</appmsg>
<fromusername>wenoptics</fromusername>
<scene>0</scene>
<appinfo>
    <version>1</version>
    <appname></appname>
</appinfo>
<commenturl></commenturl>
</msg>
"""


class TestParse_url(TestCase):
    def test_parse_url(self):
        url = parse_url(xml_str)
        self.assertEqual(url, 'https://link.clashroyale.com/invite/friend/cn?tag=8YVGLC8C&amp;token=3kk7dc7h&amp;platform=iOS')


