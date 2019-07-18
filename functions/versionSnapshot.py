import json
jsonArray = []
with open("jsons/tjson2.json", "r") as read_file:
    data = json.load(read_file)


def versionSnapshot(json, itemname, v):
    """Returns timestamps"""

    if type(json) == unicode:
        return json

    elif type(json) == list:
        return json

    else:

        for key, value in json.iteritems():

            # print key, value

            if "Item" in key:

                name = key.replace('Item', '')

                version = name+"Versions"
                timestamp = value["timestamp"]
                data = value[version][v]["data"]
                ts = value[version][v]["timestamp"]
                s = versionSnapshot(data, itemname, v)

            else:

                if type(value) == unicode:
                    s = versionSnapshot(value, itemname, v)

                elif type(value) == list:

                    s = versionSnapshot(value, itemname, v)

                    for i in range(0, len(s)):

                        for k, v in s[i].iteritems():

                            if k == "timestamp":
                                newjson = {}
                                newjson.update({"data": {itemname: {}}})
                                newjson.update({"timestamp": v})

                                jsonArray.append(newjson)

                elif type(value) == dict:
                    for k, v in value.iteritems():
                        s = versionSnapshot(v, itemname, v)

    return jsonArray


def preprocess_json_array(arr, itemname):
    """Pre process the timestamps returned by timeSnapshot & return
     json skeleton in which data will be populated by timeSnapshot2"""

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
        final_json.update({"data": {itemname: {}}})
        final_json.update({"timestamp": newArr[t]})
        json_array.append(final_json)

    return json_array


def checkOverlap(json1, json2):

    startA, endA = json1['timestamp'].split('-')
    startB, endB = json2['timestamp'].split('-')

    if (startA == startB) or (startB < startA <= endB):
        return True
    else:
        return False


def give_recursive_items2(arr, d, i, t):

    item = arr[i]
    for key, value in d.iteritems():
        # print key,value

        if "Item" in key:
            # print k1
            name = key.replace('Item', '')
            version = name+"Versions"

            if name == item:
                for versions in value[version]:

                    for k, v in versions.iteritems():
                        # print k, v
                        # print t, v
                        if k == 'timestamp' and checkOverlap(t, str(v)) == True:
                            if i+1 == len(arr):
                                dict1 = {key:''}

                                dict1[key]=value
                                return dict1


                            else:
                                return give_recursive_items2(arr, versions['data'][item], i+1, t)


def versionSnapshot2(json, json1, itemname):
    """Populates the json skeleton returned by preprocess_json_array() """

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
                    s = versionSnapshot2(data, json1, itemname)
            else:

                if type(value) == unicode:
                    s = versionSnapshot2(value, json1, itemname)

                elif type(value) == list:

                    s = versionSnapshot2(value, json1, itemname)

                    for i in range(0, len(s)):

                        if s[i]['timestamp'] == json1['timestamp'] or checkOverlap(json1, s[i]) is True:

                            for k, v in s[i].iteritems():

                                if k != 'timestamp':
                                    for k2, v2 in v.iteritems():

                                        json1["data"][itemname].update({k2: v2})

                elif type(value) == dict:
                    for k, v in value.iteritems():
                        s = versionSnapshot2(v, json1, itemname)

    return json1


if __name__ == '__main__':

    new = []
    itemname = 'specimen'

    """input"""
    items = ['specimen', 'name']
    t = '2016-2018'

    arr = versionSnapshot(data, items[-1], 0)

    output_json_arr = preprocess_json_array(arr, items[-1])

    newdata = give_recursive_items2(items, data, 0, t)

    for j in range(0, len(output_json_arr)):

        ss = versionSnapshot2(newdata, output_json_arr[j], itemname)
        new.append(ss)

    # print new

    # with open('versionSnap.json', 'w') as fp:
    #     json.dump(new, fp)
