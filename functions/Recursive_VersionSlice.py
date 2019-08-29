import csv
import json
import os
import time


class VersionSlice:

    def __init__(self):
        pass

    def versionslice(self, arr, d, i):

        item = arr[i]
        for key, value in d.iteritems():

            if "Item" in key:

                name = key.replace('Item', '')
                version = name + "Versions"

                if name == item:

                    for versions in value[version]:

                        for k, v in versions.iteritems():

                            if k == 'timestamp':

                                if i+1 == len(arr):

                                    t = value['timestamp']

                                    if t not in flags or flags[t] == 'False':

                                        dict1 = {key: value}
                                        output_array.append(dict1)
                                        flags[t] = 'True'

                                else:

                                    self.versionslice(arr, versions['data'][item], i+1)
        return output_array


if __name__ == '__main__':

    obj = VersionSlice()
    path = '/Users/mymac/Documents/GitHub/Research/Experiments/reversed_JSON/reversed_parent_change_folder'
    save_path = '/Users/mymac/Documents/GitHub/Research/Experiments/parent_change/parent_change_folder_Version_slice'

    fields = ['time', 'changes']
    csv_name = "/Users/mymac/Documents/GitHub/Research/Experiments/CSV/VersionSlice/Versionslice_time_log_small.csv"
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

                    # Specify version number here
                    ver = 99

                    item = items[-1]+'Item'
                    version = items[-1]+'Versions'

                    output_array = []
                    versionArray = []
                    flags = {}
                    flags2 = {}

                    slices = obj.versionslice(items, data, 0)

                    for dicts in slices:
                        for arrays in dicts[item][version]:
                            t = arrays['timestamp']
                            if t not in flags2 or flags2[t] == 'False':

                                versionArray.append(arrays)
                                flags2[t] = 'True'

                    slice_dict = {}

                    timestamp = versionArray[0]['timestamp']
                    version_slice = versionArray[ver]

                    slice_dict.update({"specimenItem": {"timestamp": timestamp, "specimenVersions": [version_slice]}})

                    with open(save_path+'/'+file_names, 'w') as fp:
                        json.dump(mydict, fp)

                    end = time.time()
                    diff = end-start
                    print file_names
                    print(end - start)
                    print "----------------------------------------------------------------------------------------"

                    versions = file_names.replace(".json", "")

                    rows.append([diff, versions])

    with open(csv_name, 'w') as csv_file:

        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(fields)
        csv_writer.writerows(rows)
