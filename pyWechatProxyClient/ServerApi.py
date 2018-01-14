import json

from pyWechatProxyClient.api.model.Message import Message


def parse_message(str_message: str):
    """
    parse str_message to wechat message sent by WechatProxy server
    :param str_message:
    :return:
    """
    try:
        d_msg = json.loads(str_message)
        wx_message = Message()
        wx_message.set_message(
            talker_id=d_msg.get('sender'),
            time=d_msg.get('time'),
            content=d_msg.get('content'),
        )
        return wx_message
    except:
        import traceback
        print('parse msg failed. {}'.format(traceback.format_exc()))
        return None
