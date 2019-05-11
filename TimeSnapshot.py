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
    json = json.load(read_file)


def timeSnapshot(json):
    result = []
    if json == str:
        print "inside base condition"
        # n = [Node(json, None, json, None)]
        # result.append(n)
        return json

    elif type(json) == list:
        for i in json:
            s = timeSnapshot(i)
            result.append(Node("list", None, s, None))

    else:
        for key, value in json.iteritems():

            print "KEYYYYYY", key
            print "VALUEEEE", value
            if "Item" in key:
                name = key.replace('Item', '')

                version = name+"Versions"
                timestamp = value["timestamp"]

                for versions in value[name+"Versions"]:

                    data = versions["data"]
                    ts = versions["timestamp"]

                    # print data
                    # print ts
                    s = timeSnapshot(data)
                    # node = Node("interiorList", None, s, ts)
                    # result.append(node)

            else:
                if type(value)==str:
                    print value
                    # node = Node("string", None, value, None)
                    # result.append([node])

                elif type(value)==list:
                    for element in value:
                        s = timeSnapshot(element)
                        # node = Node("list", None, s, None)
                        # result.append(node)

                elif type(value)==dict:
                    # for k, v in value.iteritems():

                    s = timeSnapshot(value)
                    # print s
                    # for k, v in value.iteritems():
                    #     s = timeSnapshot(k)
                    #     node = Node("pair", k, s, None)
                    #     result.append(node)


timeSnapshot(json)


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



















