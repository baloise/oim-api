from workflows.Workflows import GenericWorkflow, CreateVmWorkflow, WorkflowTypes
from models.orders import OrderType, Order, CreateOrder, DeleteOrder, ModifyOrder, Person
from app import db


class WorkflowFactory:

    def __init__(self):
        self._creators = {}
        self.register_workflow(WorkflowTypes.WF_GENERIC, GenericWorkflow)
        self.register_workflow(WorkflowTypes.WF_CREATE_VM, CreateVmWorkflow)

    def register_workflow(self, workflow_type: WorkflowTypes, workflowClass: GenericWorkflow):
        self._creators[workflow_type] = workflowClass

    def get_workflow(self, workflow_type):
        creator = self._creators.get(workflow_type)
        if not creator:
            raise ValueError(workflow_type)
        wf = creator()
        return wf


class OrderFactory:

    def __init__(self):
        self._creators = {}
        self.register_type(OrderType.CREATE_ORDER, CreateOrder)
        self.register_type(OrderType.DELETE_ORDER, DeleteOrder)
        self.register_type(OrderType.MODIFY_ORDER, ModifyOrder)

    def register_type(self, order_type: OrderType, orderClass: Order):
        self._creators[order_type] = orderClass

    def get_order(self, order_type: OrderType, items, requester: Person):
        creator = self._creators.get(order_type)
        if not creator:
            raise ValueError(order_type)
        new_order = creator(order_type, items, requester)
        db.session.add(new_order)
        db.session.commit()
        return new_order
