import json

name = ''
newdata = {}
result = []


with open("tjson.json", "r") as read_file:
    data = json.load(read_file)


def timeSnapshot(json):

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

                newdata.update({"data": {"specimen": {}}})

                for versions in value[version]:

                    data = versions["data"]
                    ts = versions["timestamp"]
                    s = timeSnapshot(data)
                    print s

            else:

                if type(value) == unicode:
                    s = timeSnapshot(value)
                    # print "unicode", s

                elif type(value) == list:

                    s = timeSnapshot(value)

                    for i in range(0, len(s)):

                        for k, v in s[i].iteritems():

                            if k == "timestamp":
                                newdata.update({"timestamp": v})
                            if type(v) == dict:
                                for k2, v2 in v.iteritems():
                                    newdata["data"]["specimen"].update({k2: v2})

                elif type(value) == dict:
                    for k, v in value.iteritems():
                        s = timeSnapshot(v)

    return newdata



jsonData = timeSnapshot(data)

with open('result.json', 'w') as fp:
    json.dump(jsonData, fp)




























