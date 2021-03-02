import queue
from threading import Thread
from threading import Event
from ourCloud.OurCloudHandler import OurCloudRequestHandler
import logging
from oim_logging import get_oim_logger
import time
from typing import Tuple
import requests
import json

# type alias
Param = Tuple[str]


class doubleQuoteDict(dict):

    def __str__(self):
        return json.dumps(self)

    def __repr__(self):
        return json.dumps(self)


class RunnerThread(Thread):
    StopEvent = 0

    def __init__(self, queue, event, finalStatus, queryParams):
        Thread.__init__(self)
        self.queue = queue
        self.StopEvent = event
        self.finalStatus = finalStatus
        self.queryParams = queryParams

    # The run method is overridden to define
    # the thread body
    def run(self):
        reqno = self.queue.get()
        handler = OurCloudRequestHandler.getInstance()
        if self.finalStatus:
            currentStatus = handler.get_request_status(reqno)
            while currentStatus != self.finalStatus:
                if(self.StopEvent.wait(0)):
                    info = "Thread {} detected stop event, terminating gracefully...".format(self.name)
                    logging.getLogger(get_oim_logger()).info(info)
                    break

                info = "Received status '{current}' of request {reqno} not equal to final status '{status}', waiting...".format(  # noqa: E501
                        status=self.finalStatus, reqno=reqno, current=currentStatus)
                logging.getLogger(get_oim_logger()).info(info)
                time.sleep(5)
                currentStatus = handler.get_request_status(reqno)
            else:
                info = "Received status '{current}' of request {reqno} is final status '{status}'".format(  # noqa: E501
                        status=self.finalStatus, reqno=reqno, current=currentStatus)
                logging.getLogger(get_oim_logger()).info(info)
        try:
            ocdetails = handler.get_extended_request_parameters(reqno, self.queryParams)
            info = "Polled extended parameters values of request {reqno}: {ocstatus}".format(ocstatus=ocdetails,
                                                                                             reqno=reqno)
            logging.getLogger(get_oim_logger()).info(info)
            self.send_request(reqno, ocdetails)
        except Exception as e:
            logging.getLogger(get_oim_logger()).error(e)
        finally:
            logging.getLogger(get_oim_logger()).info("Polling completed")
            self.queue.task_done()

    def send_request(self, requestno, details: dict):
        # Now we start building the request to the backend
        url = "http://localhost:9090/oc/v0.1/oc/request/details"

        jsonObj = {}
        jsonObj["requestno"] = "{r}".format(r=requestno)
        jsonObj["details"] = []
        for key in details.keys():
            jsonObj["details"].append({
                "attribute_name": key,
                "attribute_value": details[key]
            })
        logging.getLogger(get_oim_logger()).debug("before: {b}".format(b=jsonObj))
        payload = json.dumps(doubleQuoteDict(jsonObj))
        logging.getLogger(get_oim_logger()).debug("after: {a}".format(a=payload))

        headers = {
            "Content-Type": "application/json"
        }

        # Send the request to the backend
        info = "Send details to url {url} : {det}".format(url=url, det=payload)
        logging.getLogger(get_oim_logger()).info(info)
        try:
            response = requests.post(url, headers=headers, data=payload)
        except Exception as e:
            logging.getLogger(get_oim_logger()).error(e)
        else:
            # Ensure response looks valid
            if not response.status_code == 200:
                error = "An error occured ({code}): {txt}".format(code=response.status_code, txt=response.text)
                logging.getLogger(get_oim_logger()).error(error)
                return ""
            info = "Details have been sent back successfully ({code})".format(code=response.status_code)
            logging.getLogger(get_oim_logger()).info(info)


class OurCloudStatusProducer:

    def __init__(self, statusParameters: Param, *, finalStatus: str):
        self.queue = queue.Queue(maxsize=0)
        self.queryParams = statusParameters
        self.finalStatus = finalStatus
        self.statusParameters = statusParameters
        # worker = Thread(target=self.do_poll, args=(self.queue,))
        # worker.setDaemon(True)
        # worker.start()

    def pollStatus(self, reqno):
        self.queue.put(reqno)
        Stop = Event()
        workerThread = RunnerThread(self.queue, Stop, self.finalStatus, self.statusParameters)
        try:
            workerThread.start()
            while workerThread.is_alive():
                # Try to join the child thread back to parent for 0.5 seconds
                workerThread.join(0.5)
        except KeyboardInterrupt:
            # Set the stop event
            Stop.set()
            info = "Main thread asked child {} to stop".format(workerThread.name)
            logging.getLogger(get_oim_logger()).info(info)
            # Block until child thread is joined back to the parent
            workerThread.join()

        self.queue.join()
