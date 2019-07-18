import csv
import json
import collections
import os
import time


def checkOverlap(json1, json2):

    startA, endA = json1.split('-')
    startB, endB = json2.split('-')

    if (startA == startB) or (startB < startA <= endB) or (startB>startA and endA==endB):
        return True
    else:
        return False


def get_keylist(array):
    # Determine numbers of versions

    keyarray = []
    keydict = {}

    for i in array:
        # keyarray.append(i['data']['specimen'].keys())

        keydict[tuple(i['data']['specimen'].keys())] = True

    # print "keydict", keydict

    # print "here,,,", len(keyarray), keyarray
    #
    # i = 0
    #
    # while i < len(keyarray)-1:
    #     j = i+1
    #     if keyarray[i] == keyarray[j]:
    #         keyarray.remove(keyarray[i])
    #
    #     i += 1

    # for i in range(0, len(keyarray) - 1):
    #     for j in range(i + 1, len(keyarray)):
    #         if keyarray[i] == keyarray[j]:
    #             keyarray.remove(keyarray[i])
    # print "helo...", keyarray

    for k, v in keydict.iteritems():
        keyarray.append(list(k))
    return keyarray


def create_skeleton(keylist):

    pjson = {}
    pjson.update({"specimenItem": {"timestamp": " ", "specimenVersions": []}})

    for i in range(0, len(keylist)):
        pjson['specimenItem']['specimenVersions'].append({})

    arr=[]
    for j in keylist:

        vdict = {}
        vdict.update({"timestamp":"", 'data': {'specimen': {}}})
        for k in j:
            itemname = k+'Item'
            num = 0
            while num < len(keylist):

                vdict["data"]["specimen"].update({itemname: ''})
                num = num+1

        arr.append(vdict)

    pjson['specimenItem']['specimenVersions'] = arr

    return pjson


def getTimestamps(data):
    """Iterating through the snapshots json to retrieve timestamps. If the keys are different then add timestamp
     to time array else add to merge array. Merge array timestamps will be later reduced to one timestamp as the
    keys didn't change this merged timestamp will be the timestamp for new version."""

    timearray=[]
    mergearray = []

    # key1 = data[0]['data']['specimen'].keys()
    # key1 = ['colloquial', 'name', 'surname', 'dummy']
    # print "1st key", key1

    # timearray.append(data[0]['timestamp'])

    for k in range(-1, len(data)-1):

        if collections.Counter(data[k]['data']['specimen'].keys()) == collections.Counter(data[k+1]['data']['specimen'].keys()):

            # print "is equal", collections.Counter(data[k]['data']['specimen'].keys()), collections.Counter(data[k+1]['data']['specimen'].keys())

            # print data[k]['timestamp']
            # key1 = collections.Counter(data[k]['data']['specimen'].keys())
            if not mergearray.__contains__(data[k]['timestamp']):
                mergearray.append(data[k]['timestamp'])
                mergearray.append(data[k+1]['timestamp'])
        else:
            # print " Not equal", collections.Counter(data[k]['data']['specimen'].keys()), collections.Counter(data[k+1]['data']['specimen'].keys())
            timearray.append(data[k]['timestamp'])
        # key1 = collections.Counter(data[k]['data']['specimen'].keys())

    small = []
    large = []

    # print "here...", mergearray, timearray

    if mergearray!=[]:
        for i in range(0, len(mergearray)):

            minimum, maximum = mergearray[i].split('-')
            small.append(int(minimum))
            large.append(int(maximum))

        t = str(min(small))+'-'+str(max(large))
        timearray.append(t)

    return timearray


def populate_data(myjson):

    arr = myjson['specimenItem']['specimenVersions']

    for i in range(0, len(timearr)):
        for j in range(0, len(arr)):

            arr[i]['timestamp'] = timearr[i]

    for i in range(0, len(myjson['specimenItem']['specimenVersions'])):

        for k, v in arr[i]['data']['specimen'].iteritems():

            version = str(k).replace('Item', 'Versions')

            arr[i]['data']['specimen'][k] = {'timestamp': '', version: []}

    # print "arr == ", arr, len(data)

    for j in range(0, len(arr)):

        for time in range(0, len(data)):

            # print "data--1", data[time]['data']
            # print "data--2", arr[j]['data']
            # print data[time]['timestamp'], arr[j]['timestamp']
            # print "-----------------------------------------------------"

            if checkOverlap(data[time]['timestamp'], arr[j]['timestamp']):

                for key, val in arr[j]['data']['specimen'].iteritems():

                    for k, v in data[time]['data']['specimen'].iteritems():

                        # print "key==", k+'Item', key

                        if k+'Item' == key:

                            mydict = {}

                            t = data[time]['timestamp']

                            mydict.update({'timestamp': t, 'data': {k: v}})
                            # print mydict, t
                            ver = k+'Versions'

                            arr[j]['data']['specimen'][key][ver].append(mydict)

                            # print "here......", arr[j]['data']['specimen'][key][ver]

    return myjson


def fix_timestamps(myjson):
    ar = myjson['specimenItem']['specimenVersions']
    for i in range(0, len(ar)):
        t = ar[i]['timestamp']
        for k, v in ar[i]['data']['specimen'].iteritems():

            v['timestamp'] = t
    small = []
    big = []
    for t in range(0, len(ar)):

        mini, maxi = ar[t]['timestamp'].split('-')
        small.append(int(mini))
        big.append(int(maxi))

    t = str(min(small))+'-'+str(max(big))
    myjson['specimenItem']['timestamp'] = t

    return myjson


path = '/Users/mymac/Documents/GitHub/Research/Experiments/child_change_folder_medium'
save_path = '/Users/mymac/Documents/GitHub/Research/Experiments/reversed_child_change_folder_medium'

fields = ['time', 'versions']

csv_name = "reverse_child_chnge_time_log_medium.csv"

rows = []
# with open('/Users/mymac/Documents/GitHub/Research/Experiments/child_change_folder_large/100.json', "r") as read_file:
#     data = json.load(read_file)
for file in sorted(os.listdir(path)):

    full_filename = "%s/%s" % (path, file)

    with open(full_filename, "r") as read_file:

        start = time.time()

        data = json.load(read_file)

        timearr = getTimestamps(data)

        keylist = get_keylist(data)

        myjson = create_skeleton(keylist)

        myjson = populate_data(myjson)

        myjson = fix_timestamps(myjson)

        with open(save_path+'/'+file, 'w') as fp:

            json.dump(myjson, fp)

        end = time.time()

        diff = end-start

        versions = file.replace(".json", "")

        rows.append([diff, versions])

        print diff, versions, full_filename

with open(csv_name, 'w') as csvfile:

    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(rows)



















