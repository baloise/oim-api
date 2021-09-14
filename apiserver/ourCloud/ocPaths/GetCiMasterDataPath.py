from ourCloud.ocPaths.AbstractOcPath import AbstractOcPath
import requests


class GetCiMasterDataPath(AbstractOcPath):
    # 3.4.4

    def __init__(self, object_name, object_type='VM'):
        """Creates the path object to retrieve CI master data for a specific object

        Parameters
        ----------
        object_name : str
            Name of object to retrieve
            Format: "servername"
        object_type : str, optional
            Type of object to retrieve (Default: 'VM')
        """
        self.object_name = object_name
        self.object_type = object_type
        super().__init__()

    def get_url(self, object_name, object_type) -> str:
        # /V2/CI/GetCIMasterData/ObjectId/VMNAMEHERE/ObjectType/VM
        url = f'{self.get_base_url()}/V2/CI/GetCIMasterData/ObjectId/{object_name}/ObjectType/{object_type}'
        return url

    def send_request(self, ) -> str:
        url = self.get_url(self.object_name, self.object_type)
        responseRaw = requests.request(
            "GET",
            url,
            headers=self.get_header(),
            verify=self.get_verify(),
        )
        # method_json_query = "[?RequestNo == `{no}`].{attribute}|[0]".format(no=self.requestno, attribute='Status')
        method_json_query = ''
        return self.getResultJson(responseRaw, method_json_query)
