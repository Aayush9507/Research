import csv
import json
import os
import time


class TimeSnapshot:

    def get_timestamps(self, json, itemname):

        """Retrieves all the timestamps present in the JSON"""
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

                        s = self.get_timestamps(data, itemname)

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

    def pre_process_timestamps(self, arr, itemname, input_t):

        """Prepossesses all the timestamps from get_timestamps() and returns an array of JSON's containing only
        those timestamps which are required for Time Snapshots. Creates a Skeleton which will be later populated"""

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
                newArr.append(str(smallest_start) + '-' + smallest_end)

            smallest_start = int(smallest_end) + 1

        json_array = []

        for t in range(0, len(newArr)):
            if self.check_overlap2(newArr[t], input_t):
                final_json = {}
                final_json.update({"data": {itemname: {}}})
                final_json.update({"timestamp": newArr[t]})
                json_array.append(final_json)

        return json_array

    def check_overlap2(self, json1, json2):
        """Checks whether two timestamps overlap"""

        startA, endA = json1.split('-')
        startB, endB = json2.split('-')

        if (startA == startB) or (startB < startA <= endB) or (startB > startA and endA == endB) or endB < endA and startB > startA:
            return True
        else:

            return False

    def check_overlap(self, json1, json2):
        """Checks whether two timestamps overlap"""

        startA, endA = json1['timestamp'].split('-')
        startB, endB = json2['timestamp'].split('-')

        if (startA == startB) or (startB < startA <= endB) or (startB > startA and endA == endB):
            return True
        else:
            return False

    def give_recursive_items2(self, arr, d, i, t):
        """Recursively deep dives into parent item until the requested item is found,
        updates JSON after each recursive call"""

        item = arr[i]
        for key, value in d.iteritems():

            if "Item" in key:
                name = key.replace('Item', '')
                version = name+"Versions"

                if name == item:

                    for versions in value[version]:

                        for k, v in versions.iteritems():

                                if k == 'timestamp' and t != '' and v != '' and self.check_overlap2(t, unicode(v)):

                                    if i+1 == len(arr):

                                        dict1 = {key: value}
                                        return dict1

                                    else:

                                        return self.give_recursive_items2(arr, versions['data'][item], i+1, t)

    def utility(self, dict):
        for key, value in dict.iteritems():

            v = key.replace('Item', 'Versions')

            arr = value[v]

            for d in range(0, len(arr)):
                for k, v in arr[d].iteritems():

                    if k != 'timestamp':
                        return v

    def populate_data(self, parent, json1, itemname):
        """Performs final step, which is to populate the skeleton with data from temporal JSON"""

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


if __name__ == '__main__':

    obj = TimeSnapshot()
    path = '/Users/mymac/Documents/GitHub/Research/Experiments/reversed_JSON/reversed_parent_change_all'
    save_path = '/Users/mymac/Documents/GitHub/Research/Experiments/parent_change/parent_change_folder_Time_snapshots_all'

    with open('/Users/mymac/Documents/GitHub/Research/jsons/tjson2.json', "r") as read_file:
        data = json.load(read_file)

    fields = ['time', 'size']
    csv_name = "Timesnapshot_Parentchange_SizeVsTime.csv"
    rows = []

    for file_names in sorted(os.listdir(path)):
        if not file_names.startswith('.'):
            full_filename = "%s/%s" % (path, file_names)
            with open(full_filename, "r") as read_file:
                data = json.load(read_file)

                for file in data:
                    start = time.time()

                    jsonArray = []

                    """inputs"""
                    itemname = 'specimen'
                    input_array = ['specimen']
                    input_timestamp = '1000-9000'

                    working_data = obj.give_recursive_items2(input_array, data, 0, input_timestamp)

                    output = []
                    all_timestamps = obj.get_timestamps(working_data, itemname)

                    skeleton = obj.pre_process_timestamps(all_timestamps, itemname, input_timestamp)

                    for j in range(0, len(skeleton)):

                        if obj.check_overlap2(skeleton[j]['timestamp'], input_timestamp):

                            snapshot = obj.populate_data(working_data, skeleton[j], itemname)
                            output.append(snapshot)

                    print "--------------------Snapshot ------------------------"

                    with open(save_path+'/'+file_names, 'w') as fp:
                        json.dump(output, fp)

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
