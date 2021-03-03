from . import AbstractOcPath
import requests


class GetRequestStatusPath(AbstractOcPath.AbstractOcPath):
    # 3.4.4

    def __init__(self, requestno):
        if not requestno:
            raise ValueError("No request number provided")
        self.requestno = requestno
        super().__init__()

    def get_url(self) -> str:
        return '{baseUrl}/Requests/Request'.format(
                    baseUrl=self.get_base_url()
                )

    def send_request(self) -> str:
        responseRaw = requests.request("GET", self.get_url(), headers=self.get_header(), data=self.get_body(),
                                       verify=False)
        method_json_query = "[?RequestNo == `{no}`].{attribute}|[0]".format(no=self.requestno, attribute='Status')
        return self.getResultJson(responseRaw, method_json_query)
