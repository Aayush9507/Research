import csv
import json
import os
import time


class VersionSnapshot:

    def __init__(self):
        pass

    def get_timestamps(self, json, itemname):

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

                        newjson = {}
                        newjson.update({"data": {itemname: {}}})
                        newjson.update({"timestamp": ts})
                        if newjson not in jsonArray:
                            jsonArray.append(newjson)

                else:

                    if type(value) == unicode:
                        s = self.get_timestamps(value, itemname)

                    elif type(value) == list:

                        s = self.get_timestamps(value, itemname)

                        for i in range(0, len(s)):

                            if type(s[i]) != unicode:
                                for k, v in s[i].iteritems():

                                    if k == "timestamp":
                                        newjson = {}
                                        newjson.update({"data": {itemname: {}}})
                                        newjson.update({"timestamp": v})

                                        if newjson not in jsonArray:
                                            jsonArray.append(newjson)

                    elif type(value) == dict:
                        for k, v in value.iteritems():
                            s = self.get_timestamps(v, itemname)

        return jsonArray

    def pre_process_json_array(self, arr, itemname):

        res_list = []
        for i in range(len(arr)):
            if arr[i] not in arr[i + 1:]:
                res_list.append(arr[i])

        startArr = []
        endArr = []

        for j in range(0, len(res_list)):
            if str(res_list[j]['timestamp']) != '':
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

                newArr.append(str(smallest_start) + '-' + str(smallest_end))
                smallest_start = int(smallest_end) + 1

        json_array = []

        for t in range(0, len(newArr)):

                final_json = {}
                final_json.update({"data": {itemname: {}}})
                final_json.update({"timestamp": newArr[t]})
                json_array.append(final_json)

        return json_array

    def check_overlap2(self, json1, json2):

        startA, endA = json1.split('-')
        startB, endB = json2.split('-')

        if (startA == startB) or (startB < startA <= endB) or (startB>startA and endA==endB) or endB<endA and startB>startA:
            return True
        else:

            return False

    def check_overlap(self, json1, json2):

        startA, endA = json1['timestamp'].split('-')
        startB, endB = json2['timestamp'].split('-')

        if (startA == startB) or (startB < startA <= endB) or (startB>startA and endA==endB) :
            return True
        else:
            return False

    def utility(self, dict):
        for key, value in dict.iteritems():

            v = key.replace('Item', 'Versions')

            arr = value[v]

            for d in range(0, len(arr)):
                for k, v in arr[d].iteritems():

                    if k != 'timestamp':
                        return v

    def populate_data(self, parent, json1, itemname):

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
                        s = self.populate_data(data, json1, itemname)

                else:

                    if type(value) == unicode and key == itemname:
                        if self.check_overlap2(json1['timestamp'], ts) or json1['timestamp'] == ts:

                            json1["data"].update({key: value})

                    if type(value) == list and key == itemname:

                        if json1['timestamp'] == ts or self.check_overlap2(json1['timestamp'], ts):

                            json1["data"].update({key: value})

                    elif type(value) == list:

                        s = self.populate_data(value, json1, itemname)

                        for i in range(0, len(s)):

                            if s[i]['timestamp'] == json1['timestamp'] or self.check_overlap(json1, s[i]) is True:

                                for k, v in s[i].iteritems():

                                    if k != 'timestamp':
                                        for k2, v2 in v.iteritems():

                                            if type(v2) == dict:

                                                getvalues = self.utility(v2)
                                                json1["data"][itemname].update({k2: getvalues})

                                            else:

                                                json1["data"][itemname].update({k2: v2})

                    elif type(value) == dict:
                        for k, v in value.iteritems():
                            s = self.populate_data(v, json1, itemname)

        return json1

    def give_recursive_items(self, arr, d, i):

        item = arr[i]
        for key, value in d.iteritems():

            if "Item" in key:

                name = key.replace('Item', '')
                version = name+"Versions"

                if name == item:

                    for versions in range(0, len(value[version])):

                        for k, v in value[version][versions].iteritems():

                            if k == 'timestamp':

                                if i+1 == len(arr):

                                    dict1 = {key: value}
                                    arrr.append(dict1)

                                else:

                                    self.give_recursive_items(arr, value[version][versions]['data'][item], i + 1)
        return arrr


if __name__ == '__main__':

    obj = VersionSnapshot()
    path = '/Users/mymac/Documents/GitHub/Research/Experiments/reversed_JSON/reversed_parent_change_all'
    save_path = '/Users/mymac/Documents/GitHub/Research/Experiments/parent_change/parent_change_folder_Version_snapshots_all'

    fields = ['time', 'size']
    csv_name = "VersionSnapshot_ParentChange_SizeVsTime.csv"
    rows = []

    for file_names in sorted(os.listdir(path)):

        if not file_names.startswith('.'):
            full_filename = "%s/%s" % (path, file_names)
            print full_filename
            with open(full_filename, "r") as read_file:
                data = json.load(read_file)

                for file in data:
                    start = time.time()

                    jsonArray = []

                    itemname = 'specimen'

                    """input"""
                    items = ['specimen']
                    input_version = 82

                    arrr = []

                    newdata = obj.give_recursive_items(items, data, 0)

                    for i in range(0, len(newdata)):
                        arr = obj.get_timestamps(newdata[i], itemname)

                    output_json_arr = obj.pre_process_json_array(arr, itemname)

                    new = {}

                    for i in range(0, len(newdata)):
                        snapshot = obj.populate_data(newdata[i], output_json_arr[input_version], itemname)

                    print "--------------------Snapshot ------------------------"

                    with open(save_path+'/'+file_names, 'w') as fp:
                        json.dump(snapshot, fp)

                    end = time.time()

                    print file_names
                    print(end - start)

                    diff = end-start
                    versions = file_names.replace(".json", "")

                    rows.append([diff, os.path.getsize(full_filename)/1024])

    with open(csv_name, 'w') as csvfile:

        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)
