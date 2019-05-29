import json

with open("tjson2.json", "r") as read_file:
    data = json.load(read_file)

mydict = {}


def versionslice(json, version):

    arr = json['specimenItem']['specimenVersions']
    return arr[version]


vslice = versionslice(data, 0)
timestamp = vslice['timestamp']
mydict.update({"specimenItem": {"timestamp": timestamp, "specimenVersions": [vslice]}})


with open('versionslice2.json', 'w') as fp:

    json.dump(mydict, fp)




