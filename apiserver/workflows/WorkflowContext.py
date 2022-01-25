from models.orders import Person
from models.orders import OrderItem
from typing import List
from itsm.ConfigItems import SystemConfigItem


class WorkflowContextItem:
    def __init__(self, changeno: str, item: OrderItem):
        self.wfitem = {'id': item.id, 'changeno': changeno}

    def getItemId(self) -> str:
        return self.wfitem['id']

    def getItemChangeno(self) -> str:
        return self.wfitem['changeno']


class WorkflowContext:
    def __init__(self, requester: Person):
        self.requester = requester
        self.changeno = None
        self.items = []
        self.itemDetails = {}

    def get_requester(self):
        return self.requester

    def set_changeno(self, changeno: str):
        self.changeno = changeno

    def get_changeno(self):
        return self.changeno

    def add_item(self, item: OrderItem, changeno: str):
        wfitem = WorkflowContextItem(changeno, item)
        self.items.append(wfitem)

    def get_items(self) -> List[WorkflowContextItem]:
        return self.items

    def getItemChangeno(self, item: OrderItem):
        for itm in self.items:
            oid = itm.getItemId()
            if oid == item.id:
                return itm.getItemChangeno()
        return None

    def updateItemDetails(self, item: OrderItem, details: SystemConfigItem):
        self.itemDetails.update({item.id: details})

    def getItemDetails(self, item: OrderItem) -> SystemConfigItem:
        return self.itemDetails.get(item.id, None)
