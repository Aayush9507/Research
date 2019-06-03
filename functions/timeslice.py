import json

with open("jsons/tjson2.json", "r") as read_file:
    data = json.load(read_file)

mydict = {}


def checkOverlap(json1, json2):

    startA, endA = json1.split('-')
    startB, endB = json2.split('-')

    if (startA == startB) or (startB < startA <= endB):
        return True
    else:
        return False


def timeslice(json,t):

    arr = json['specimenItem']['specimenVersions']

    for i in range(0, len(arr)):

        if checkOverlap(t, arr[i]["timestamp"]):

            return arr[i]["data"]


string = "2015-2015"
tslice = timeslice(data, string)

timestamp = string
mydict.update({"specimenItem": {"timestamp": timestamp, "specimenVersions": [tslice]}})

with open('TESTtimeslice.json', 'w') as fp:

    json.dump(mydict, fp)



