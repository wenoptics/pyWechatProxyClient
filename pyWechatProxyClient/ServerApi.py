import json

import datetime

import re


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
            internal_type=d_msg.get('type')
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


class ServerApiConst:
    INTERNAL_TYPE_TEXT = 1
    INTERNAL_TYPE_PHOTO = 3
    INTERNAL_TYPE_SHARING = 49
    INTERNAL_TYPE_STICKER = 47
