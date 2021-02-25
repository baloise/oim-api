import queue
from threading import Thread
from ourCloud.OurCloudHandler import OurCloudRequestHandler
import logging
import time
from typing import Tuple

# type alias
Param = Tuple[str]


class OurCloudStatusProducer:

    def do_poll(self, q):
        while True:
            reqno = q.get()
            handler = OurCloudRequestHandler.getInstance()
            if self.finalStatus:
                currentStatus = handler.get_request_status(reqno)
                while currentStatus != self.finalStatus:
                    logging.debug("Received status '{current}' not equal to final status '{status}', waiting...".format(  # noqa: E501
                        status=self.finalStatus, current=currentStatus))
                    time.sleep(5)
                    currentStatus = handler.get_request_status(reqno)
                else:
                    logging.debug("Received status '{current}' is final status '{status}'".format(  # noqa: E501
                        status=self.finalStatus, current=currentStatus))
            try:
                ocdetails = handler.get_extended_request_parameters(reqno, self.queryParams)
            except Exception as e:
                logging.error(e)
            else:
                info = "Polled extended parameters values of request {reqno}: {ocstatus}".format(ocstatus=ocdetails,
                                                                                                 reqno=reqno)
                logging.info(info)
            finally:
                logging.debug("Polling completed")
                q.task_done()

    def __init__(self, statusParameters: Param, *, finalStatus: str):
        self.q = queue.Queue(maxsize=0)
        self.queryParams = statusParameters
        self.finalStatus = finalStatus
        num_threads = 1
        for i in range(num_threads):
            worker = Thread(target=self.do_poll, args=(self.q,))
            worker.setDaemon(True)
            worker.start()

    def pollStatus(self, reqno):
        self.q.put(reqno)
        self.q.join()
