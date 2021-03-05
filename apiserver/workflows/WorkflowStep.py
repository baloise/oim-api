from typing import List
import collections
import enum
from workflows.steps.WorkflowSteps import DeployItemStep, AbstractWorkflowStep


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

    def execute(self):
        for step in self.steps:
            try:
                step.execute()
            except Exception:
                break

    def __iter__(self):
        ''' Returns the Iterator object '''
        return BatchIterator(self)


class Workflow:

    def get_name(self):
        return self.name

    def __init__(self, name: str, is_repeatable=False):
        self.batches: DeepChainMap = None
        self.name = name

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

    def execute(self):
        if self.batches is None:
            return
        maplist = self.batches.maps
        maplist.sort()
        for batch in maplist:
            try:
                batch.execute()
            except Exception:
                break
