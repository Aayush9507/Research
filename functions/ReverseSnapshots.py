import collections
import json
import os
import time
import csv


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

        keydict[tuple(i['data']['specimen'].keys())] = True

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

            if not mergearray.__contains__(data[k]['timestamp']):
                mergearray.append(data[k]['timestamp'])
            if not mergearray.__contains__(data[k+1]['timestamp']):
                mergearray.append(data[k]['timestamp'])
                # mergearray.append(data[k+1]['timestamp'])
        else:
            timearray.append(data[k]['timestamp'])

    small = []
    large = []

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

    for i in range(0, len(data)):
        for j in range(0, len(arr)):

            dummy = arr[j]['data']['specimen'].copy()

            for k in dummy.keys():
                dummy[k.replace("Item", "")] = dummy.pop(k)

            # print set(dummy.keys()) == set(data[i]['data']['specimen'].keys())
            diff = set(dummy.viewkeys()) - set(data[i]['data']['specimen'].keys())
            # if len(diff)==0:
            #
            #     print "sperator"
            #     print dummy.keys()
            #     print "---------------"
            #     print data[i]['data']['specimen'].keys()
            #     print "sperator"

            # print len(set(dummy.keys())), len(set(data[i]['data']['specimen'].keys()))
            # print dummy.keys()
            # print data[i]['data']['specimen'].keys()
            # print set(dummy.keys()) == set(data[i]['data']['specimen'].keys())
            # print "---------------------------------"
            # if [x.replace('Item', '') for x, v in arr[j]['data']['specimen'].items()] == data[i]['data']['specimen'].keys():

            # if set(dummy.keys()) == set(data[i]['data']['specimen'].keys()):
            if len(diff)==0:
                # print True

                if data[i]['timestamp'] in timearr:
                    arr[j]['timestamp'] = data[i]['timestamp']

    for i in range(0, len(arr)):

        for k, v in arr[i]['data']['specimen'].iteritems():

            version = str(k).replace('Item', 'Versions')

            arr[i]['data']['specimen'][k] = {'timestamp': '', version: []}

    for j in range(0, len(arr)):

        for time in range(0, len(data)):

            if type(arr[j]['timestamp']) == unicode and type(data[time]['timestamp']) == unicode:

                if checkOverlap(data[time]['timestamp'], arr[j]['timestamp']):

                    for key, val in arr[j]['data']['specimen'].iteritems():

                        for k, v in data[time]['data']['specimen'].iteritems():

                            if k+'Item' == key:

                                mydict = {}

                                t = data[time]['timestamp']

                                mydict.update({'timestamp': t, 'data': {k: v}})
                                ver = k+'Versions'

                                arr[j]['data']['specimen'][key][ver].append(mydict)

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
        if ar[t]['timestamp'] != '':
            mini, maxi = ar[t]['timestamp'].split('-')
            small.append(int(mini))
            big.append(int(maxi))

    t = str(min(small))+'-'+str(max(big))
    myjson['specimenItem']['timestamp'] = t

    return myjson


def remove_empty_dictionaries(myjson):

    arr = myjson['specimenItem']['specimenVersions']
    for i in arr:
        if type(i['timestamp']) != unicode:
            arr.remove(i)
    return myjson


path = '/Users/mymac/Documents/GitHub/Research/Experiments/parent_change_folder_large'
save_path = '/Users/mymac/Documents/GitHub/Research/Experiments/reversed_parent_change_folder_large'

fields = ['time', 'versions']

csv_name = "reverse_time_log_large.csv"

rows = []

for file in sorted(os.listdir(path)):

    full_filename = "%s/%s" % (path, file)

    with open(full_filename, "r") as read_file:

        start = time.time()

        data = json.load(read_file)

        timearr = getTimestamps(data)

        keylist = get_keylist(data)

        myjson = create_skeleton(keylist)

        # print "skeleton", myjson
        myjson = populate_data(myjson)

        # print myjson

        myjson = fix_timestamps(myjson)

        myjson = remove_empty_dictionaries(myjson)

        # print myjson

        with open(save_path+'/'+file, 'w') as fp:

            json.dump(myjson, fp)

        end = time.time()

        diff = end-start

        versions = file.replace(".json", "")

        rows.append([diff, versions])

        print diff, versions, full_filename
#
# with open(csv_name, 'w') as csvfile:
#
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(fields)
#     csvwriter.writerows(rows)


















