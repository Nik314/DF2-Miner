import pm4py

from src import df2_miner_apply
from src.ocpn_conversion import convert_ocpt_to_ocpn

ocpt = df2_miner_apply("data/running-example.jsonocel",activity_coverage=0.95)
ocpn, convergent = convert_ocpt_to_ocpn(ocpt)

print(str(ocpt))

#ocpn is a dictionary with a Petri net for each type
#convergent shows the variable arcs per object type
print(convergent)

#for ot,net in ocpn.items():
#    pm4py.view_petri_net(*net)
#(shows workflow net per type)

