import csv
import json
import os
import time


class TimeSlice:

    def __init__(self):
        pass

    def check_overlap2(self, json1, json2):

        startA, endA = json1.split('-')
        startB, endB = json2.split('-')

        if startA == startB or startB < startA <= endB or startB > startA and endA == endB or endB < endA and startB > startA:
            return True
        else:
            return False

    def time_slice(self, arr, d, timestamp, i):

        item = arr[i]
        for key, value in d.iteritems():

            if "Item" in key:

                name = key.replace('Item', '')
                version = name+"Versions"

                if name == item:

                    for versions in range(0, len(value[version])):

                        for k, v in value[version][versions].iteritems():

                            if k == 'timestamp' and v != '' and timestamp != '':
                                if self.check_overlap2(v, timestamp):

                                    if i+1 == len(arr):

                                        dict1 = {key: value}
                                        arrr.append(dict1)

                                    else:

                                        self.time_slice(arr, value[version][versions]['data'][item], timestamp, i+1)
        return arrr


if __name__ == '__main__':

    obj = TimeSlice()
    path = '/Users/mymac/Documents/GitHub/Research/Experiments/reversed_JSON/reversed_child_change_folder_large'
    save_path = '/Users/mymac/Documents/GitHub/Research/Experiments/child_change/child_change_folder_Time_slice_large'

    fields = ['time', 'versions']
    csv_name = "Timeslice_childchange_time_log_large.csv"
    rows = []
    mydict = {}

    for file_names in sorted(os.listdir(path)):

        if not file_names.startswith('.'):
            original_timestamp = ''
            tslice = ''

            full_filename = "%s/%s" % (path, file_names)
            with open(full_filename, "r") as read_file:
                data = json.load(read_file)

                for file in data:
                    start = time.time()

                    items = ['specimen']
                    arrr = []

                    # Input Timestamp here
                    timestamp = '1299-1299'

                    slices = obj.time_slice(items, data, timestamp, 0)

                    item = items[-1]+'Item'
                    version = items[-1]+'Versions'

                    for i in range(0, len(slices)):
                        for j in slices[i][item][version]:
                            if j['timestamp'] != '' and timestamp != '':
                                if obj.check_overlap2(j['timestamp'], timestamp):
                                    tslice = j
                                    original_timestamp = j['timestamp']

                    mydict.update({item: {"timestamp": original_timestamp, version: [tslice]}})

                    with open(save_path+'/'+file_names, 'w') as fp:
                        json.dump(mydict, fp)

                    end = time.time()
                    diff = end-start
                    print file_names
                    print(end - start)

                    versions = file_names.replace(".json", "")

                    rows.append([diff, versions])

    with open(csv_name, 'w') as csvfile:

        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)





