import json

f = open('/Users/bakhyt17/Documents/python_projects/lab4/JSON/sample-data.json')

json_dict = json.load(f)

interface = """
Interface Status
================================================================================
DN                                                 Description           Speed    MTU  
-------------------------------------------------- --------------------  ------  ------
"""

print(interface,end="")
n = 0
for i in json_dict['imdata']:
    print(i['l1PhysIf']['attributes']['dn'], '\t\t\t\t', i['l1PhysIf']['attributes']['descr'],i['l1PhysIf']['attributes']['speed'],i['l1PhysIf']['attributes']['mtu'])
    n += 1
    if n==3:
        break

f.close()