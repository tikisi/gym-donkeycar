import json
import logging
import requests
import time
from threading import Thread

logger = logging.getLogger(__name__)


class HttpClient:
    def __init__(self, host, port, poll_socket_sleep_time=0.05):
        self.msg = None
        self.host = host
        self.port = port
        self.poll_socket_sleep_sec = poll_socket_sleep_time
        self.th = None

        self.aborted = False
        self.connect()

    def connect(self):
        self.do_process_msgs = True
        self.th = Thread(target=self.proc_msg, args=(), daemon=True)
        self.th.start()

    def send(self, m):
        self.msg = m

    def on_msg_recv(self, j):
        logger.debug("got:" + j["msg_type"])

    def stop(self):
        self.do_process_msgs = False
        if self.th is not None:
            self.th.join()

    def proc_msg(self):
        while self.do_process_msgs:
            time.sleep(self.poll_socket_sleep_sec)

            if self.msg is None:
                continue

            logger.debug("sending " + self.msg)
            print(self.msg)
            response = requests.post("http://172.17.0.1:8082/test_api", self.msg)
            self.msg = None

            j = response.json()
            if "msg_type" in j:
                self.on_msg_recv(j)