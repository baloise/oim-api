import queue
from threading import Thread
from ourCloud.OurCloudHandler import OurCloudRequestHandler
import logging


class OurCloudStatusProducer:

    def do_poll(self, q):
        while True:
            reqno = q.get()
            # print(reqno)
            handler = OurCloudRequestHandler.getInstance()
            try:
                extendedParams = ["RequestDetailID", "InstanceSize", "hdnOSType"]
                ocdetails = handler.get_extended_request_parameters(reqno, extendedParams)
            except Exception as e:
                logging.error(e)
            else:
                info = "Request {reqno} extended parameters values: {ocstatus}".format(ocstatus=ocdetails, reqno=reqno)
                logging.info(info)
            finally:
                logging.debug("All tasks completed")
                q.task_done()

    def __init__(self):
        self.q = queue.Queue(maxsize=0)
        num_threads = 1
        for i in range(num_threads):
            worker = Thread(target=self.do_poll, args=(self.q,))
            worker.setDaemon(True)
            worker.start()

    def pollStatus(self, reqno):
        self.q.put(reqno)
        self.q.join()
