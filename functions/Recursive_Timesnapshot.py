import csv
import json
import os
import time


def timeSnapshot(json, itemname):

    global ts
    global newjson

    if type(json) == unicode:
        return json

    elif type(json) == list:
        return json

    else:

        for key, value in json.iteritems():

            if "Item" in key:

                name = key.replace('Item', '')
                version = name+"Versions"

                for versions in value[version]:

                    data = versions["data"]
                    ts = versions["timestamp"]

                    s = timeSnapshot(data, itemname)

                    newjson={}
                    newjson.update({"data": {itemname: {}}})
                    newjson.update({"timestamp": ts})
                    jsonArray.append(newjson)

            else:

                if type(value) == unicode:
                    s = timeSnapshot(value, itemname)

                elif type(value) == list:

                    s = timeSnapshot(value, itemname)

                    for i in range(0, len(s)):

                        if type(s[i]) != unicode:
                            for k, v in s[i].iteritems():

                                if k == "timestamp":
                                    newjson = {}
                                    newjson.update({"data": {itemname: {}}})
                                    newjson.update({"timestamp": v})

                                    jsonArray.append(newjson)

                elif type(value) == dict:
                    for k, v in value.iteritems():
                        s = timeSnapshot(v, itemname)

    return jsonArray


def preprocess_json_array(arr, itemname, input_t):

    res_list = []
    for i in range(len(arr)):
        if arr[i] not in arr[i + 1:]:
            res_list.append(arr[i])

    startArr = []
    endArr = []

    for j in range(0, len(res_list)):
        if str(res_list[j]['timestamp'])!='':
            start, end = str(res_list[j]['timestamp']).split("-")

            startArr.append(start)

            endArr.append(end)

    newArr = []

    smallest_start = min(startArr)
    max_end = max(endArr)

    while int(smallest_start) <= int(max_end):

        smallest_end = min(endArr)
        endArr.remove(smallest_end)
        if int(smallest_start) <= int(smallest_end):
            newArr.append(str(smallest_start) + '-' + smallest_end)

        smallest_start = int(smallest_end) + 1

    json_array = []

    for t in range(0, len(newArr)):
        # print newArr[t], input_t
        if checkOverlap2(newArr[t], input_t):
            final_json = {}
            final_json.update({"data": {itemname: {}}})
            final_json.update({"timestamp": newArr[t]})
            json_array.append(final_json)

    return json_array


def checkOverlap2(json1, json2):

    startA, endA = json1.split('-')
    startB, endB = json2.split('-')

    if (startA == startB) or (startB < startA <= endB) or (startB>startA and endA==endB) or endB<endA and startB>startA:
        return True
    else:

        return False


def checkOverlap(json1, json2):

    startA, endA = json1['timestamp'].split('-')
    startB, endB = json2['timestamp'].split('-')

    if (startA == startB) or (startB < startA <= endB) or (startB>startA and endA==endB):
        return True
    else:
        return False


def give_recursive_items2(arr, d, i, t):

    item = arr[i]
    for key, value in d.iteritems():

        if "Item" in key:
            name = key.replace('Item', '')
            version = name+"Versions"

            if name == item:

                for versions in value[version]:

                    for k, v in versions.iteritems():

                            if k == 'timestamp' and t!='' and v!='' and checkOverlap2(t, unicode(v)):

                                if i+1 == len(arr):

                                    dict1 = {key:''}
                                    dict1[key] = value
                                    return dict1

                                else:

                                    return give_recursive_items2(arr, versions['data'][item], i+1, t)


def utility(dict):
    for key, value in dict.iteritems():

        v = key.replace('Item', 'Versions')

        arr = value[v]

        for d in range(0, len(arr)):
            for k, v in arr[d].iteritems():

                if k!='timestamp':
                    return v


def timeSnapshot2(parent, json1, itemname):

    global ts

    if type(parent) == unicode:
        return parent

    elif type(parent) == list:
        return parent

    else:

        for key, value in parent.iteritems():

            if "Item" in key:
                name = key.replace('Item', '')
                v = name+"Versions"
                t = value["timestamp"]

                for versions in range(0, len(value[v])):

                    data = value[v][versions]["data"]
                    ts = value[v][versions]["timestamp"]
                    s = timeSnapshot2(data, json1, itemname)

            else:

                if type(value) == unicode and key == itemname:
                     if checkOverlap2(json1['timestamp'], ts) or json1['timestamp'] == ts:

                        json1["data"].update({key: value})

                if type(value) == list and key == itemname:

                    if json1['timestamp'] == ts or checkOverlap2(json1['timestamp'], ts):

                        json1["data"].update({key: value})
                        # print json1

                elif type(value) == list:

                    s = timeSnapshot2(value, json1, itemname)

                    for i in range(0, len(s)):

                        if s[i]['timestamp'] == json1['timestamp'] or checkOverlap(json1, s[i]) is True:

                            for k, v in s[i].iteritems():

                                if k != 'timestamp':
                                    for k2, v2 in v.iteritems():

                                        if type(v2) == dict:

                                            getvalues = utility(v2)
                                            json1["data"][itemname].update({k2: getvalues})

                                        else:

                                            json1["data"][itemname].update({k2: v2})

                elif type(value) == dict:
                    for k, v in value.iteritems():
                        s = timeSnapshot2(v, json1, itemname)
                        # print s

    return json1


if __name__ == '__main__':

    path = '/Users/mymac/Documents/GitHub/Research/Experiments/reversed_parent_change_folder'
    save_path = '/Users/mymac/Documents/GitHub/Research/Experiments/child_change_folder_Time_snapshots_small'

    with open('/Users/mymac/Documents/GitHub/Research/jsons/tjson2.json', "r") as read_file:
        data = json.load(read_file)

    fields = ['time', 'versions']
    csv_name = "Timesnapshot_childchng_time_log_small.csv"
    rows = []

    for file_names in os.listdir(path):

        full_filename = "%s/%s" % (path, file_names)
        with open(full_filename, "r") as read_file:
            data = json.load(read_file)

            # print data

            for file in data:
                start = time.time()

                jsonArray = []

                itemname = 'specimen'

                """input"""
                items = ['specimen']
                input_t = '1000-9000'

                arrr = []

                newdata = give_recursive_items2(items, data, 0, input_t)

                # print newdata

                new = []
                arr = timeSnapshot(newdata, itemname)

                print len(arr)

                output_json_arr = preprocess_json_array(arr, itemname, input_t)

                print output_json_arr
    #
    #             for j in range(0, len(output_json_arr)):
    #
    #                 if checkOverlap2(output_json_arr[j]['timestamp'], input_t):
    #
    #                     ss = timeSnapshot2(newdata, output_json_arr[j], itemname)
    #                     new.append(ss)
    #
    #             print "--------------------Snapshot ------------------------"
    #             print new
    #
    #             with open(save_path+'/'+file_names, 'w') as fp:
    #                 json.dump(new, fp)
    #
    #             end = time.time()
    #
    #             print file_names
    #             print(end - start)
    #
    #             diff = end-start
    #             versions = file_names.replace(".json", "")
    #
    #             rows.append([diff, versions])
    #
    # with open(csv_name, 'w') as csvfile:
    #
    #     csvwriter = csv.writer(csvfile)
    #     csvwriter.writerow(fields)
    #     csvwriter.writerows(rows)
