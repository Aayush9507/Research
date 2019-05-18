import json

name = ''
newjson = {}
result = []
jsonArray = []

with open("tjson2.json", "r") as read_file:
    data = json.load(read_file)


def timeSnapshot(json):

    if type(json) == unicode:
        return json

    elif type(json) == list:
        return json

    else:

        for key, value in json.iteritems():

            if "Item" in key:
                # print key
                name = key.replace('Item', '')
                version = name+"Versions"
                timestamp = value["timestamp"]

                # newjson.update({"data": {"specimen": {}}})


                for versions in value[version]:

                    data = versions["data"]
                    ts = versions["timestamp"]
                    s = timeSnapshot(data)
                    # print s
            else:

                if type(value) == unicode:
                    s = timeSnapshot(value)
                    # print "unicode", s

                elif type(value) == list:

                    s = timeSnapshot(value)

                    # print "list", s

                    for i in range(0, len(s)):

                        # print type(s[i]), s[i]

                        # print sorted(s[i])
                        for k, v in s[i].iteritems():

                            if k == "timestamp":
                                # print k, v
                                newjson = {}
                                newjson.update({"data": {"specimen": {}}})
                                newjson.update({"timestamp": v})
                                # newjson2.update({"timestamp": v})

                                # print newjson
                                jsonArray.append(newjson)

                            # if type(v) == dict:
                            #     for k2, v2 in v.iteritems():
                            #
                            #         print k2, v2



                                    # newjson["data"]["specimen"].update({k2: v2})



                                    # print "new", newjson

                elif type(value) == dict:
                    for k, v in value.iteritems():
                        s = timeSnapshot(v)
                        # print s

    return jsonArray


arr = timeSnapshot(data)


def preprocess_json_array(arr):

    res_list = []
    for i in range(len(arr)):
        if arr[i] not in arr[i + 1:]:
            res_list.append(arr[i])

    startArr = []
    endArr = []

    for i in range(0, len(res_list)):
        start, end = str(res_list[i]['timestamp']).split("-")
        startArr.append(start)
        endArr.append(end)

    newArr = []
    smallest_start = min(startArr)
    max_end = max(endArr)


    while int(smallest_start) <= int(max_end):
        smallest_end = min(endArr)
        endArr.remove(smallest_end)
        newArr.append(str(smallest_start) + '-' + smallest_end)
        smallest_start = int(smallest_end) + 1

    json_array = []

    for t in range(0, len(newArr)):

        final_json = {}
        final_json.update({"data": {"specimen": {}}})
        final_json.update({"timestamp": newArr[t]})
        json_array.append(final_json)

    return json_array


output_json_arr =  preprocess_json_array(arr)


for o in range(0, len(output_json_arr)):

    print output_json_arr[o]


    # jsonData = timeSnapshot(data)
#
# with open('result2.json', 'w') as fp:
#     json.dump(jsonData, fp)


def timeSnapshot2(json):

    if type(json) == unicode:
        return json

    elif type(json) == list:
        return json

    else:

        for key, value in json.iteritems():

            if "Item" in key:
                # print key
                name = key.replace('Item', '')
                version = name+"Versions"
                timestamp = value["timestamp"]

                # newjson.update({"data": {"specimen": {}}})


                for versions in value[version]:

                    data = versions["data"]
                    ts = versions["timestamp"]
                    s = timeSnapshot2(data)
                    # print s
            else:

                if type(value) == unicode:
                    s = timeSnapshot2(value)
                    # print "unicode", s

                elif type(value) == list:

                    s = timeSnapshot2(value)

                    # print "list", s

                    for i in range(0, len(s)):

                        if s[i]['timestamp']==json1['timestamp']:

                            for k, v in s[i].iteritems():

                                if k != 'timestamp':
                                    for k2, v2 in v.iteritems():

                                        json1["data"]["specimen"].update({k2: v2})

                    print "jsonnn", json1

                elif type(value) == dict:
                    for k, v in value.iteritems():
                        s = timeSnapshot2(v)
                        # print s

    # return json1


# timeSnapshot2(data)


















