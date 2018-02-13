import base64
import json
import datetime
import logging
import re

import os

from pyWechatProxyClient.api.consts import PICTURE
from pyWechatProxyClient.api.model.Message import Message

logger = logging.getLogger(__name__)


def parse_message(str_message: str):
    """
    parse str_message to wechat message sent by WechatProxy server
    :param str_message:
    :return:
    """
    try:
        d_msg = json.loads(str_message)

        time = parse_time(d_msg.get('time'))

        from pyWechatProxyClient.api.model.Message import Message
        wx_message = Message()

        wx_message.set_message(
            talker_id=d_msg.get('sender'),
            time=time,
            content=d_msg.get('content'),
            internal_type=d_msg.get('type'),
            talker_nickname=d_msg.get('senderNickname'),
            chatroom_talkerid=d_msg.get('chatroomSender'),
            chatroom_talker_nickname=d_msg.get('chatroomSenderNickname'),
        )
        return wx_message
    except:
        import traceback
        print('parse msg failed. {}'.format(traceback.format_exc()))
        return None


def parse_time(s: str):
    """

    :param s:
    :return: datetime.datetime
    """
    try:
        timestamp = int(s) / 1000
        ret = datetime.datetime.fromtimestamp(timestamp)
        return ret
    except:
        import traceback
        print('parse_time failed. {}'.format(traceback.format_exc()))
        return None


def parse_url(xml_str: str):
    try:
        found = re.search(r'<url>(.*?)</url>', xml_str)
        return found.group(1)
    except:
        import traceback
        print('parse_url failed. {}'.format(traceback.format_exc()))
        return None


def make_message(msg: Message):
    
    assert msg.sender

    content = msg.text
    if msg.type == PICTURE:
        # Decode the image data with base64
        assert os.path.isfile(msg.text)
        content = base64.b64encode(open(msg.text, 'rb').read()).decode()
        logger.debug('encoded string len==%d', len(content))

    d = {
        'sender': msg.sender.talker_id,
        'content': content,
        # Currently only support IMAGE or TEXT
        'type': ServerApiConst.API_IMAGE_ONLY if msg.type == PICTURE else ServerApiConst.API_TEXT_ONLY
    }
    return json.dumps(d)


class ServerApiConst:
    INTERNAL_TYPE_TEXT = 1
    INTERNAL_TYPE_PHOTO = 3
    INTERNAL_TYPE_SHARING = 49
    INTERNAL_TYPE_STICKER = 47
    INTERNAL_TYPE_SYSTEM = 10000

    API_TEXT_ONLY = 0
    API_IMAGE_ONLY = 1
