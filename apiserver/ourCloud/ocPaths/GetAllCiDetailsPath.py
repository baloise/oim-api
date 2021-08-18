from ourCloud.ocPaths.AbstractOcPath import AbstractOcPath
import requests


class GetAllCiDetailsPath(AbstractOcPath):
    # 3.4.4

    def __init__(self, data_filter=''):
        """Generates path object to retrieve ci details about either all
        or a filtered subset of CI's

        Parameters
        ----------
        data_filter : str, optional
            Optional datafilter to limit the list to. (Default '')
            Format: "RequestNo='162'"
        """
        self.data_filter = data_filter
        super().__init__()

    def get_url(self) -> str:
        # /V2/CI/GetAllCIDetails/OrgEntityId/:OrgEntityId/
        url = f'{self.get_base_url()}/V2/CI/GetAllCIDetails/OrgEntityId/{self.getOrgEntityId()}/'
        return url

    def send_request(self) -> str:
        url = self.get_url()
        if self.data_filter:
            url += f"?datafilter={self.data_filter}"
        responseRaw = requests.request(
            "GET",
            url,
            headers=self.get_header(),
            verify=self.get_verify(),
        )
        # method_json_query = "[?RequestNo == `{no}`].{attribute}|[0]".format(no=self.requestno, attribute='Status')
        method_json_query = ""
        return self.getResultJson(responseRaw, method_json_query)
