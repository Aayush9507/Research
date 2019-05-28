import json
from datadiff import diff


with open("s1", "r") as read_file:
    json1 = json.load(read_file)


with open("s2", "r") as read_file:
    json2 = json.load(read_file)


delta = diff(json1, json2)
print delta

with open('delta.json', 'w') as fp:

    json.dump(str(delta), fp)



