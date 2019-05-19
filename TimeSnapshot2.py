import json
jsonArray = []


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

                # print key
                name = key.replace('Item', '')
                version = name+"Versions"
                timestamp = value["timestamp"]

                for versions in value[version]:

                    data = versions["data"]
                    ts = versions["timestamp"]
                    s = timeSnapshot(data)
            else:

                if type(value) == unicode:
                    s = timeSnapshot(value)

                elif type(value) == list:

                    s = timeSnapshot(value)

                    for i in range(0, len(s)):

                        for k, v in s[i].iteritems():

                            if k == "timestamp":
                                newjson = {}
                                newjson.update({"data": {"specimen": {}}})
                                newjson.update({"timestamp": v})

                                jsonArray.append(newjson)

                elif type(value) == dict:
                    for k, v in value.iteritems():
                        s = timeSnapshot(v)

    return jsonArray


arr = timeSnapshot(data)


def preprocess_json_array(arr):

    res_list = []
    for i in range(len(arr)):
        if arr[i] not in arr[i + 1:]:
            res_list.append(arr[i])

    startArr = []
    endArr = []

    for j in range(0, len(res_list)):
        start, end = str(res_list[j]['timestamp']).split("-")

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


output_json_arr = preprocess_json_array(arr)


for o in range(0, len(output_json_arr)):

    json1 = output_json_arr[o]
    break


def checkOverlap(json1,json2):

    startA, endA = json1['timestamp'].split('-')
    startB, endB = json2['timestamp'].split('-')

    if (startA==startB) or (startA>startB and startA<=endB):
        return True
    else:
        return False


def timeSnapshot2(json):

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
                    s = timeSnapshot2(data)
            else:

                if type(value) == unicode:
                    s = timeSnapshot2(value)

                elif type(value) == list:

                    s = timeSnapshot2(value)

                    for i in range(0, len(s)):

                        if s[i]['timestamp']==json1['timestamp'] or checkOverlap(json1, s[i])==True:

                            for k, v in s[i].iteritems():

                                if k != 'timestamp':
                                    for k2, v2 in v.iteritems():

                                        json1["data"]["specimen"].update({k2: v2})



                elif type(value) == dict:
                    for k, v in value.iteritems():
                        s = timeSnapshot2(v)
                        # print s

    return json1


ss = timeSnapshot2(data)

with open('result.json', 'w') as fp:
    json.dump(ss, fp)


















