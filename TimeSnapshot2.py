import json
from objdict import ObjDict


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



    name=''
    newdata={}

    result = []
    if type(json) == unicode:
        return json

    elif type(json) == list:
        return json

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
                    # print s
                    # result.append(node)

            else:

                if type(value) == unicode:
                    s = timeSnapshot(value)
                    # print "unicode", s


                elif type(value) == list:

                    newdata.update({"data":{}})
                    newdata['data'].update({'specimen':{}})
                    s = timeSnapshot(value)
                    # print "list", s
                    for i in range(0, len(s)):

                        # print s[i]
                        for k, v in s[i].iteritems():

                            # print k, v

                            if k == "timestamp":
                                # print v
                                newdata.update({"timestamp":v})


                            if type(v) == dict:
                                for k2, v2 in v.iteritems():

                                    # print k2,v2
                                    # print "......"

                                    newdata['data']['specimen'][k2]=v2
                                    print "new json ", newdata


                elif type(value) == dict:
                    for k, v in value.iteritems():
                        s = timeSnapshot(v)
                        # print "dict", s


    # return result
    # print newdata






res = timeSnapshot(data)


























