from collections import namedtuple
import simplejson
import json

class Node:

    def __init__(self, t, k, v, ts):

        self.t = t
        self.k = k
        self.v = v
        self.ts = ts

# with open('tjson.json') as f:
#     myjson = simplejson.load(f, object_hook=lambda d: namedtuple('foo', d.keys())(*d.values()))

with open("tjson.json", "r") as read_file:
    data = json.load(read_file)


def timeSnapshot(json):
    result = []
    if json == str:

        n = [Node(json, None, json, None)]
        result.append(n)
        return result

    elif type(json) == list:
        for i in json:
            s = timeSnapshot(i)
            result.append(Node("list", None, s, None))

    else:
        for key, value in json.iteritems():
            if "Item" in key:
                name = key.replace('Item', '')

                version = name+"Versions"
                timestamp = value["timestamp"]
                print version, timestamp
                
                print value[version]



timeSnapshot(data)


# with open("tjson.json", "r") as read_file:
#     data = json.load(read_file)
#     val = data["specimenItem"]
#
#     v = data["specimenItem"]["specimenVersions"][0]["data"]["specimen"]
#     for key, val in v.iteritems():
#         print key
#         if "Item" in str(key):
#             print True
        # for k, v in val.iteritems():
        #     print k, v



















