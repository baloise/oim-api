from workflows.WorkflowStep import Workflow, Batch, BatchPhase
from workflows.steps.WorkflowSteps import DeployItemStep, DummyStep, VerifyItemStep
import collections
from models.my_orders import Person, SbuType, OrderItemType, OrderStateType, OrderItem, OrderStatus, Order  # noqa: F401,E501


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


di1 = {"k1": "v1"}
di2 = {"k2": "v2"}

map = DeepChainMap(di1)
map = map.new_child(di2)
map.maps = reversed(map.maps)
# print(map)

personPeter = Person(
            username='u12345',
            email='peter.parker@test.fake',
            sbu=SbuType.SHARED
        )

rhel_item = OrderItem("rhel8", OrderItemType.DMY)
items = [rhel_item]
new_order = Order(items, personPeter)

bat_pre = Batch("pre-work", BatchPhase.RE_VERIFICATION, False)
step1 = DummyStep("verify request")
bat_pre.add_step(step1)

bat_depl = Batch("deploy", BatchPhase.BE_PROCESSING, False)
for it in new_order.get_items():
    step = DeployItemStep(new_order.get_items()[0])
    bat_depl.add_step(step)

bat_ver = Batch("verify", BatchPhase.BE_VERIFICATION, False)
for it in new_order.get_items():
    step = VerifyItemStep(new_order.get_items()[0])
    bat_ver.add_step(step)


bat_tst = Batch("test", BatchPhase.TESTING, False)
step4 = DummyStep("request testing")
step5 = DummyStep("receive testing status")
bat_tst.add_step(step4)
bat_tst.add_step(step5)

bat_hov = Batch("handover", BatchPhase.HANDOVER, False)
step6 = DummyStep("complete request")
bat_hov.add_step(step6)

print("Defining Workflows")

wf = Workflow("new vm")
wf.add_batch(bat_pre)
wf.add_batch(bat_depl)
wf.add_batch(bat_ver)
wf.add_batch(bat_tst)
wf.add_batch(bat_hov)

print("List Batches&their Actions {}".format(wf.get_name()))
for batch in wf.get_batches():
    print(" Batch {}".format(batch))
    for step in batch:
        print("  Action: {}".format(step.get_action()))

print("Execute Workflows")
wf.execute()

if False:
    dm = DeepChainMap()
    print("#1")
    di1 = {"wf_a": step1}
    dm = dm.new_child(di1)

    vals = list(dm.values())
    kys = list(dm.keys())
    print("Length: {}".format(len(dm.maps)))
    for kl in kys:
        print("Map KV: {}={}".format(kl, dm[kl]))

    print("#2")
    di2 = {"c": "d"}
    dm = dm.new_child(di2)
    print(len(dm.maps))

    kys = list(dm.keys())
    for kl in kys:
        print("{}={}".format(kl, dm[kl]))
print("............")
