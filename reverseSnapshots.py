import json
import collections

with open("result.json", "r") as read_file:
    data = json.load(read_file)


def get_keylist(array):
    # Determine numbers of versions

    empty = []
    for i in array:
        empty.append(i['data']['specimen'].keys())

    for i in range(0, len(empty) - 1):
        for j in range(i + 1, len(empty)):
            if empty[i] == empty[j]:
                empty.remove(empty[i])

    return empty


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
     to time array else add to merge array. Merger array timestamps will be later reduced to one timestamps as the
    keys didn't change this merged timestamp will be the  timestamp for new version."""

    timearray=[]
    mergearray = []

    key1 = data[0]['data']['specimen'].keys()
    timearray.append(data[0]['timestamp'])

    for k in range(1, len(data)):

        if collections.Counter(data[k]['data']['specimen'].keys()) == collections.Counter(key1):

            if not timearray.__contains__(data[k]['timestamp']):
                timearray.append(data[k]['timestamp'])

        else:
            mergearray.append(data[k]['timestamp'])
            key1 = data[k]['timestamp']

    small = []
    large = []
    for i in range(0, len(mergearray)):

        minimum, maximum = mergearray[i].split('-')
        small.append(int(minimum))
        large.append(int(maximum))

    t = str(min(small))+'-'+str(max(large))

    timearray.append(t)
    return timearray


timearr = getTimestamps(data)
keylist = get_keylist(data)
myjson = create_skeleton(keylist)

print myjson
print timearr


