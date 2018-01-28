# coding: utf-8
from __future__ import unicode_literals

import logging
import weakref

from pyWechatProxyClient.utils.util import force_encoded_string_output, ensure_list

logger = logging.getLogger(__name__)


class MessageConfig(object):
    """
    单个消息注册配置
    (Originally by wxpy)
    """

    def __init__(
            self, client, func,
            chats, msg_types,
            run_async, enabled
    ):
        self.client = weakref.proxy(client)
        self.func = func

        self.chats = ensure_list(chats)
        self.msg_types = ensure_list(msg_types)

        self.run_async = run_async
        self._enabled = None
        self.enabled = enabled

    @property
    def enabled(self):
        """
        配置的开启状态
        """
        return self._enabled

    @enabled.setter
    def enabled(self, boolean):
        """
        设置配置的开启状态
        """
        self._enabled = boolean
        logger.info(self)

    @force_encoded_string_output
    def __repr__(self):
        return '<{}: {}: {} ({}{})>'.format(
            self.__class__.__name__,
            self.client.server_url,
            self.func.__name__,
            'Enabled' if self.enabled else 'Disabled',
            ', Async' if self.run_async else '',
        )

    def __unicode__(self):
        return '<{}: {}: {} ({}{})>'.format(
            self.__class__.__name__,
            self.client.server_url,
            self.func.__name__,
            'Enabled' if self.enabled else 'Disabled',
            ', Async' if self.run_async else '',
        )
