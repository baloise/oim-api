from typing import List
import collections
import enum
from workflows.steps.WorkflowSteps import AbstractWorkflowStep
from models.orderTypes.OrderTypes import GenericOrder, OrderType
from workflows.steps.WorkflowSteps import DeployItemStep
from workflows.WorkflowContext import WorkflowContext
from oim_logging import get_oim_logger


class BatchPhase(enum.Enum):
    RE_VERIFICATION = 0
    BE_PROCESSING = 100
    BE_VERIFICATION = 200
    TESTING = 300
    CMDB = 400
    HANDOVER = 500


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
    def __init__(self, name, position: BatchPhase, is_repeatable=False):
        self.steps: List[AbstractWorkflowStep] = []
        self.name = name
        self.is_repeatable = is_repeatable
        self.position = position

    def __eq__(self, other):
        return ((self.name, self.position.value) == (other.name, other.position.value))

    def __ne__(self, other):
        return ((self.name, self.position.value) != (other.name, other.position.value))

    def __lt__(self, other):
        return (self.position.value < other.position.value)

    def __le__(self, other):
        return (self.position.value <= other.position.value)

    def __gt__(self, other):
        return (self.position.value > other.position.value)

    def __ge__(self, other):
        return (self.position.value >= other.position.value)

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

    def execute(self, context: WorkflowContext):
        stepCount = len(self.steps)
        logger = get_oim_logger()
        for step in self.steps:
            try:
                step.execute(context)
                stepCount -= 1
            except Exception as e:
                error = "Error while executing step: {}".format(e)
                logger.error(error)
                break
        info = "{} of {} steps completed".format(stepCount, len(self.steps))
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
    order: GenericOrder = None     # might become constructor param
    context: WorkflowContext

    def __init__(self, name: str, is_repeatable=False):
        self.batches: DeepChainMap = None
        self.name = name

    def get_context(self):
        return self.context

    def set_context(self, context: WorkflowContext):
        self.context = context

    def get_order(self) -> GenericOrder:
        return self.order

    def set_order(self, order: GenericOrder):
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
            return
        batches_maplist = self.batches.maps
        batches_maplist.sort()
        batchCount = len(self.batches.maps)
        logger = get_oim_logger()
        for batch in batches_maplist:
            try:
                batch.execute(self.context)
                batchCount -= 1
            except Exception as e:
                error = "Error while executing batch: {}".format(e)
                logger.error(error)
                break
        info = "{} of {} batches completed".format(batchCount, len(self.batches.maps))
        logger.debug(info)
        if batchCount < len(self.batches.maps):
            raise Exception(info)
        return info


class CreateVmWorkflow(GenericWorkflow):
    type = WorkflowTypes.WF_CREATE_VM

    def __init__(self):
        super().__init__("create vm", False)

    def set_order(self, order: GenericOrder):
        if order.get_type() == OrderType.CREATE_ORDER:
            super().set_order(order)
            batch = Batch("deploy", BatchPhase.BE_PROCESSING, False)
            for item in super().get_order().get_items():
                if item.is_Vm():
                    step = DeployItemStep(item)
                    batch.add_step(step)
            self.add_batch(batch)
