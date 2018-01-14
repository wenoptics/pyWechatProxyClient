import asyncio
import logging

import websockets


class WebSocketClientEngine:

    __server_url = 'ws://192.168.1.161:5000/wechat'
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
        self.timeout_check = 10
        self.timeout_ping_pong = 5
        self.messageQueue = asyncio.Queue()

    async def run(self):
        # Reconnect loop
        while True:
            try:
                ws = await self.get_connection()
                self.logger.info('connect to server "{}"'.format(self.__server_url))
            except:
                self.logger.error('connect to server "{}" fail.'.format(self.__server_url))
                ws = None

            # Receive message loop
            while ws is not None:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=self.timeout_check)
                except asyncio.TimeoutError:
                    # self.logger.debug('No data in {} seconds, checking the connection'.format(self.timeout_check))
                    try:
                        pong_waiter = await ws.ping()
                        await asyncio.wait_for(pong_waiter, timeout=self.timeout_ping_pong)
                    except asyncio.TimeoutError:
                        self.logger.error('No response to ping in {} seconds, assuming server down.'.format(self.timeout_ping_pong))
                        break
                else:
                    await self.messageQueue.put(msg)
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

    def start(self):
        asyncio.set_event_loop(self.event_loop)
        self.event_loop.run_until_complete(self.run())

    def stop(self):
        # todo
        pass


