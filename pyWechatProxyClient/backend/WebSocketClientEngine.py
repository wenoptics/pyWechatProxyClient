import asyncio
import logging

# Use `websocket-client` now
import websocket


class WebSocketClientEngine:
    def __init__(self, ws_url):
        self.logger = logging.getLogger(__name__)
        self.server_url = ws_url
        self.retry_connect_on_close = True
        self.ws = None

        self.__on_message_handler = []
        self.__should_stop = False

    def add_message_handler(self, handler):
        self.__on_message_handler.append(handler)

    def on_message(self, ws, message):
        self.logger.info("on_message: " + message)
        for h in self.__on_message_handler:
            try:
                h(message)
            except:
                self.logger.error('error occurred when handle message with one handler')
                import traceback
                self.logger.error(traceback.format_exc())

    def on_error(self, ws, error):
        self.logger.error("on_message: " + error)

    def on_close(self, ws):
        self.logger.info("### closed ###")
        self.ws = None

    def on_open(self, ws):
        self.logger.info("on_open")

    def start_listen(self):
        """
        Connect to server and start listen.
        This is a blocking method
        :return:
        """
        #websocket.enableTrace(True)
        self.__should_stop = False
        while self.retry_connect_on_close and not self.__should_stop:
            self.logger.info("connecting...")
            self.ws = websocket \
                .WebSocketApp(self.server_url,
                              on_message=self.on_message,
                              on_error=self.on_error,
                              on_close=self.on_close)
            self.ws.on_open = self.on_open
            self.ws.run_forever()

    def send(self, msg: str):
        if self.ws is None:
            raise RuntimeError('Websocket not connected yet!')
        self.logger.info("sending message: " + msg)
        self.ws.send(msg)

    def stop(self):
        if self.ws:
            self.__should_stop = True
            self.ws.close()
        self.ws = None
