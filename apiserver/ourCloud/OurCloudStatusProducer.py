import queue
from threading import Thread
from ourCloud.OurCloudHandler import OurCloudRequestHandler
import logging
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


class OurCloudStatusProducer:

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
        logging.debug("before: {b}".format(b=jsonObj))
        payload = json.dumps(doubleQuoteDict(jsonObj))
        logging.debug("after: {a}".format(a=payload))

        headers = {
            "Content-Type": "application/json"
        }

        # Send the request to the backend
        logging.info("Send details to url {url} : {det}".format(url=url, det=payload))
        try:
            response = requests.post(url, headers=headers, data=payload)
        except Exception as e:
            logging.error(e)
        else:
            # Ensure response looks valid
            if not response.status_code == 200:
                logging.error("An error occured ({code}): {txt}".format(code=response.status_code, txt=response.text))
                return ""
            logging.info("Details have been sent back successfully ({code})".format(code=response.status_code))

    def do_poll(self, q):
        while True:
            reqno = q.get()
            handler = OurCloudRequestHandler.getInstance()
            if self.finalStatus:
                currentStatus = handler.get_request_status(reqno)
                while currentStatus != self.finalStatus:
                    logging.debug("Received status '{current}' of request {reqno} not equal to final status '{status}', waiting...".format(  # noqa: E501
                        status=self.finalStatus, reqno=reqno, current=currentStatus))
                    time.sleep(20)
                    currentStatus = handler.get_request_status(reqno)
                else:
                    logging.debug("Received status '{current}' of request {reqno} is final status '{status}'".format(  # noqa: E501
                        status=self.finalStatus, reqno=reqno, current=currentStatus))
            try:
                ocdetails = handler.get_extended_request_parameters(reqno, self.queryParams)
            except Exception as e:
                logging.error(e)
            else:
                info = "Polled extended parameters values of request {reqno}: {ocstatus}".format(ocstatus=ocdetails,
                                                                                                 reqno=reqno)
                logging.info(info)
                self.send_request(reqno, ocdetails)
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
