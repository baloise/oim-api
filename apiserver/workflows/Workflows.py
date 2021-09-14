from typing import List
import collections
import enum
from workflows.steps.WorkflowSteps import AbstractWorkflowStep, CreateCrStep, AwaitDeployStep
from models.orders import Order, OrderStateType, OrderType, BackendType
from workflows.steps.WorkflowSteps import DeployVmStep, DummyStep
from workflows.WorkflowContext import WorkflowContext
from oim_logging import get_oim_logger
from api.util_status import create_status
import json
from exceptions.WorkflowExceptions import StepException, RequestHandlerException, WorkflowIncompleteException


class DeepChainMap(collections.ChainMap):
    'Variant of ChainMap that allows direct updates to inner scopes'

    def __setitem__(self, key, value):
        for mapping in self.maps:
            if key in mapping:
                mapping[key] = value
                return
        self.maps[0][key] = value

    def __delitem__(self, key):
        for mapping in self.maps:
            if key in mapping:
                del mapping[key]
                return
        raise KeyError(key)


class BatchIterator:
    ''' Iterator class '''
    def __init__(self, obj):
        # object reference
        self._obj = obj
        # member variable to keep track of current index
        self._index = 0

    def __next__(self):
        ''''Returns the next value from team object's lists '''
        if self._index < (len(self._obj.steps)):
            result = (self._obj.steps[self._index])
            self._index += 1
            return result
        # End of Iteration
        raise StopIteration


class Batch:
    def __init__(self, name, target_state, is_repeatable=False):
        self.steps: List[AbstractWorkflowStep] = []
        self.name = name
        self.is_repeatable = is_repeatable
        self.target_state = target_state

    def __eq__(self, other):
        return ((self.name, self.target_state) == (other.name, other.target_state))

    def __ne__(self, other):
        return ((self.name, self.target_state) != (other.name, other.target_state))

    def __lt__(self, other):
        return (OrderStateType.from_state(self.target_state) < OrderStateType.from_state(other.target_state))

    def __le__(self, other):
        return (OrderStateType.from_state(self.target_state) <= OrderStateType.from_state(other.target_state))

    def __gt__(self, other):
        return (OrderStateType.from_state(self.target_state) > OrderStateType.from_state(other.target_state))

    def __ge__(self, other):
        return (OrderStateType.from_state(self.target_state) >= OrderStateType.from_state(other.target_state))

    def __repr__(self):
        return "{}".format(self.name)

    def get_name(self):
        return self.name

    def is_repeatable(self) -> bool:
        return self.is_repeatable

    def get_steps(self):
        return self.steps

    def add_step(self, step):
        self.steps.append(step)

    def get_target_state(self):
        return self.target_state

    def get_fail_state(self):
        if OrderStateType.from_state(self.target_state) < OrderStateType.TESTING.value:
            retState = OrderStateType.BE_FAILED.state
        else:
            retState = OrderStateType.TEST_FAILED.state
        return retState

    def execute(self, context: WorkflowContext):
        processedStepCount = 0
        logger = get_oim_logger()
        for step in self.steps:
            try:
                step.execute(context)
                processedStepCount += 1
            except StepException as se:
                error = "Error while executing step: {}, order_id: {}".format(se, se.order_id)
                logger.error(error)
                raise Exception(error)  # rethow here once custom Exception is available
            except RequestHandlerException as re:
                error = "Error while executing step: {} order_id".format(re)
                logger.error(error)
        info = "  {} of {} steps completed".format(processedStepCount, len(self.steps))
        logger = get_oim_logger()
        logger.info(info)
        return info

    def __iter__(self):
        ''' Returns the Iterator object '''
        return BatchIterator(self)


class WorkflowTypes(enum.Enum):
    WF_GENERIC = "GENERIC"
    WF_CREATE_VM = "CREATE_VM"


class GenericWorkflow:
    type = WorkflowTypes.WF_GENERIC
    order: Order = None     # might become constructor param
    context: WorkflowContext

    def __init__(self, name: str, is_repeatable=False):
        self.batches: DeepChainMap = None
        self.name = name

    def get_context(self):
        return self.context

    def set_context(self, context: WorkflowContext):
        self.context = context

    def get_order(self) -> Order:
        return self.order

    def set_order(self, order: Order):
        self.order = order

    def get_name(self):
        return self.name

    def get_type(self) -> WorkflowTypes:
        return self.type

    def get_batches(self):
        if self.batches is None:
            return []
        maplist = self.batches.maps
        maplist.sort()
        return maplist

    def add_batch(self, batch):
        if self.batches is None:
            self.batches = DeepChainMap(batch)
        else:
            self.batches = self.batches.new_child(batch)

    def execute(self) -> str:
        if self.batches is None:
            return f"Workflow {self.name} has no batches"
        batches_maplist = self.batches.maps
        batches_maplist.sort()

        logger = get_oim_logger()

        currentOrder = self.order.id
        processedBatchCnt = 0
        processedBackendBatch = 0
        for batch in batches_maplist:
            info = f" Execute new batch: {batch}"
            logger.info(info)
            # update status upon start of BE
            if processedBackendBatch < 1 and batch.get_target_state() == OrderStateType.BE_DONE.state:
                statusJson = self.get_json(OrderStateType.BE_PROCESSING.state, BackendType.OURCLOUD.name, currentOrder)
                create_status(statusJson)
                processedBackendBatch += 1
            if processedBackendBatch < 1 and batch.get_target_state() == OrderStateType.TEST_SUCCEEDED.state:
                statusJson = self.get_json(OrderStateType.TESTING.state, BackendType.OURCLOUD.name, currentOrder)
                create_status(statusJson)
                processedBackendBatch += 1

            try:
                batch.execute(self.context)
                processedBatchCnt += 1
                statusJson = self.get_json(batch.get_target_state(), BackendType.OURCLOUD.name, currentOrder)
                create_status(statusJson)
            except Exception as e:
                error = "Error while executing batch: {} item ".format(e)
                logger.error(error)
                statusJson = self.get_json(batch.get_fail_state(), BackendType.OURCLOUD.name, currentOrder)
                create_status(statusJson)
                break

        info = "{} of {} batches completed".format(processedBatchCnt, len(self.batches.maps))
        logger.info(info)

        # update status after completion of BE processing
        if processedBatchCnt < len(self.batches.maps):
            statusJson = self.get_json(batch.get_fail_state(), BackendType.OURCLOUD.name, currentOrder)
            create_status(statusJson)
            msg = f" Workflow {self.name} didn't complete: {info}"
            logger.error(msg)
            raise WorkflowIncompleteException(msg)

        return info

    def get_json(self, state, system, orderid):
        st = '{"state": \"' + state + '\", \
               "system": \"' + system + '\", \
               "orderid": \"' + str(orderid) + '\"}'
        jStr = json.loads(st)
        return jStr


class CreateVmWorkflow(GenericWorkflow):
    type = WorkflowTypes.WF_CREATE_VM

    def __init__(self):
        super().__init__("create vm", False)

    def set_order(self, order: Order):
        if order.get_type() == OrderType.CREATE_ORDER:
            super().set_order(order)
            # Batch: verify incoming data for validity
            # WARNING: This may need to be moved away in front of the workflow or
            #           a state of rejection and according communication needs to
            #           be introduced somehow.
            vBatch = Batch("verify", OrderStateType.VERIFIED.state, True)
            for item in super().get_order().get_items():
                if item.is_Vm():
                    step = DummyStep()
                    vBatch.add_step(step)
            self.add_batch(vBatch)

            # Batch: open change
            croBatch = Batch("crcopen", OrderStateType.CR_CREATED.state, False)
            for item in super().get_order().get_items():
                if item.is_Vm():
                    stepCr = CreateCrStep(item)
                    croBatch.add_step(stepCr)
            self.add_batch(croBatch)

            # Batch: Trigger deployment on MyCloud
            dBatch = Batch("deploy", OrderStateType.BE_DONE.state, False)
            for item in super().get_order().get_items():
                if item.is_Vm():
                    step = DeployVmStep(item)
                    dBatch.add_step(step)
                    step = AwaitDeployStep(item)  # one item per change nr, items will be deployed sequentially only
                    dBatch.add_step(step)
                    closeCrStep = DummyStep("update cr")
                    dBatch.add_step(closeCrStep)
            self.add_batch(dBatch)

            # Add batch: data retrieval of remaining asset data from mycloud
            data_retrieval_batch = Batch('data_retrieval_from_oc', OrderStateType.CI_RETRIEVED.state, True)
            for item in super().get_order().get_items():
                if item.is_Vm():
                    step = DummyStep()
                    data_retrieval_batch.add_step(step)
            self.add_batch(data_retrieval_batch)

            # Batch: Run tests
            tBatch = Batch("test", OrderStateType.TEST_SUCCEEDED.state, True)
            for item in super().get_order().get_items():
                if item.is_Vm():
                    step = DummyStep()
                    tBatch.add_step(step)
            self.add_batch(tBatch)

            # Batch: Add/update entry in CMDB
            cBatch = Batch("cmdb", OrderStateType.CMDB_DONE.state, False)
            for item in super().get_order().get_items():
                if item.is_Vm():
                    cmdbStep = DummyStep("update cmdb")
                    cBatch.add_step(cmdbStep)
            self.add_batch(cBatch)
            # Batch: Mark the CR as closed.
            crcBatch = Batch("crclose", OrderStateType.CR_CLOSED.state, False)
            for item in super().get_order().get_items():
                if item.is_Vm():
                    crStep = DummyStep("close cr")
                    crcBatch.add_step(crStep)
            self.add_batch(crcBatch)

            # Batch: Handover to customer... create templates, mail them, or trigger customer hooks.
            hBatch = Batch("handover", OrderStateType.HANDOVER_DONE.state, False)
            for item in super().get_order().get_items():
                if item.is_Vm():
                    step = DummyStep()
                    hBatch.add_step(step)
            self.add_batch(hBatch)

            # Batch: end of workflow
            fBatch = Batch("done", OrderStateType.DONE.state, False)
            for item in super().get_order().get_items():
                if item.is_Vm():
                    step = DummyStep()
                    fBatch.add_step(step)
            self.add_batch(fBatch)
