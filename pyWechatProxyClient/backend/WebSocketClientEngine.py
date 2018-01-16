import asyncio
import logging

import websockets


class WebSocketClientEngine:
    __server_url = 'ws://'  # Something like 'ws://192.168.1.161:5000/wechat'
    __connection = None

    @staticmethod
    def set_server_url(url):
        WebSocketClientEngine.__server_url = url
        WebSocketClientEngine.reset_connection()

    @staticmethod
    async def get_connection():
        if WebSocketClientEngine.__connection is None:
            WebSocketClientEngine.__connection = await websockets.connect(WebSocketClientEngine.__server_url)
        return WebSocketClientEngine.__connection

    @staticmethod
    def reset_connection():
        WebSocketClientEngine.__connection = None

    def __init__(self, event_loop=None):
        if not event_loop:
            event_loop = asyncio.get_event_loop()
        self.event_loop = event_loop

        self._onMessageHandler = []
        self.logger = logging.getLogger(__name__)
        self.timeout_check = 30
        self.timeout_ping_pong = 5
        self.receive_message_queue = asyncio.Queue()
        self.send_message_queue = asyncio.Queue()
        self.ws = None

    async def send_routine(self):
        while True:
            try:
                msg = await asyncio.wait_for(self.send_message_queue.get(), timeout=0.5)
            except asyncio.TimeoutError:
                continue
            if not msg:
                continue
            self.logger.info('message to send in WebSocketClientEngine, msg=={}'.format(msg))
            if self.ws:
                try:
                    await self.ws.send(msg)
                except Exception:
                    import traceback
                    self.logger.error("send message failed")
                    self.logger.error(traceback.format_exc())

    async def connect_and_receive_routine(self):
        # Reconnect loop
        while True:
            try:
                ws = await self.get_connection()
                self.logger.info('connected to server "{}"'.format(self.__server_url))
            except:
                self.logger.error('connect to server "{}" fail.'.format(self.__server_url))
                ws = None
            self.ws = ws

            # Send message loop
            while True:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=self.timeout_check)
                except asyncio.TimeoutError:
                    # self.logger.debug('No data in {} seconds, checking the connection'.format(self.timeout_check))
                    try:
                        await asyncio.wait_for(ws.ping(), timeout=self.timeout_ping_pong)
                    except asyncio.TimeoutError:
                        self.logger.error(
                            'No response to ping in {} seconds, assuming server down.'.format(self.timeout_ping_pong))
                        break
                else:
                    await self.receive_message_queue.put(msg)
                    # print('received message in WebSocketClientEngine, msg=={}'.format(msg))
                    self.logger.info('received message in WebSocketClientEngine, msg=={}'.format(msg))
                    for handler in self._onMessageHandler:
                        try:
                            # todo Use async here?
                            handler(msg)
                        except:
                            import traceback
                            logging.error('error occur when processing message. {}'.format(traceback.format_exc()))

            await asyncio.sleep(2)
            self.reset_connection()
            self.logger.info('retry to connect to server...')

    def add_message_handler(self, handler):
        self._onMessageHandler.append(handler)

    def stop(self):
        self.logger.info('request engine stop')
        self.event_loop.stop()
