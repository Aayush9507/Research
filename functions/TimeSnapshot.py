import json

class Node:

    def __init__(self, t, k, v, ts):

        self.t = t
        self.k = k
        self.v = v
        self.ts = ts

    def display(self):

        print("t: %s \nk: %s \nv %s \nts %s"%(self.t, self.k, self.v, self.ts))


with open("tjson.json", "r") as read_file:
    data = json.load(read_file)


def timeSnapshot(json):
    result = []
    if type(json) == unicode:
        node = [Node("unicode", None, json, None)]
        result.append(node)

    elif type(json) == list:

        for i in range(0, len(json)):
            s = timeSnapshot(json[i])
            node = Node("list", None, s, None)
            result.append(node)

    else:
        for key, value in json.iteritems():

            if "Item" in key:
                name = key.replace('Item', '')

                version = name+"Versions"
                timestamp = value["timestamp"]

                for versions in value[version]:

                    data = versions["data"]
                    ts = versions["timestamp"]
                    s = timeSnapshot(data)
                    node = Node("interiorList", None, s, ts)
                    result.append(node)

            else:

                if type(value) == unicode:
                    node = Node("string", None, value, None)
                    result.append([node])

                elif type(value) == list:
                    for i in range(0, len(value)):
                        s = timeSnapshot(value[i])
                        node = Node("list", None, s, None)
                        result.append(node)

                elif type(value) == dict:
                    for k, v in value.iteritems():
                        s = timeSnapshot(v)
                        node = Node("pair", k, s, None)
                        result.append(node)

    return result


res = timeSnapshot(data)

for i in range(0, len(res)):
    print res[i].display()

    valueList = res[i].v

    for j in range(0, len(valueList)):
        print valueList[j].display()

        print valueList[j].v

        for k in range(0, len(valueList[j].v)):

            print type(valueList[j].v[k])
    #























