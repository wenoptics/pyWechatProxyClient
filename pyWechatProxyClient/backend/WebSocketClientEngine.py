import logging
import threading

# Use `websocket-client` now
import websocket

logger = logging.getLogger(__name__)


class WebSocketClientEngine:
    def __init__(self, ws_url):
        self.server_url = ws_url
        self.retry_connect_on_close = True
        self.ws = None

        self.__on_message_handler = []
        self.__stop_evt = threading.Event()

    def add_message_handler(self, handler):
        self.__on_message_handler.append(handler)

    def _on_message(self, ws, message):
        logger.info("on_message: " + message)
        for h in self.__on_message_handler:
            try:
                h(message)
            except:
                logger.error('error occurred when handle message with one handler')
                import traceback
                logger.error(traceback.format_exc())

    def _on_error(self, ws, error):
        logger.error("on_message: " + error)

    def _on_close(self, ws):
        logger.info("connection closed.")
        self.ws = None

    def _on_open(self, ws):
        logger.info("connected to server.")

    def start_listen(self):
        """
        Connect to server and start listen.
        This is a blocking method
        :return:
        """
        # websocket.enableTrace(True)
        self.__stop_evt.clear()
        while self.retry_connect_on_close and not self.__stop_evt.is_set():
            logger.info('connecting to "{}"'.format(self.server_url))
            self.ws = websocket \
                .WebSocketApp(self.server_url,
                              on_message=self._on_message,
                              on_error=self._on_error,
                              on_close=self._on_close)
            self.ws.on_open = self._on_open
            self.ws.run_forever()

    def send(self, msg: str):
        if self.ws is None:
            raise RuntimeError('Websocket not connected yet!')
        logger.info("sending message: " + msg)
        self.ws.send(msg)

    def stop(self):
        self.__stop_evt.set()
        if self.ws:
            self.ws.close()
        self.ws = None
