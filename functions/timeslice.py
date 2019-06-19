import json

with open("/Users/mymac/Documents/GitHub/Research/jsons/tjson2.json", "r") as read_file:
    data = json.load(read_file)

mydict = {}


def checkOverlap2(json1, json2):

    startA, endA = json1.split('-')
    startB, endB = json2.split('-')

    if (startA == startB) or (startB < startA <= endB) or (startB>startA and endA==endB) or endB<endA and startB>startA:
        return True
    else:

        return False


def timeslice(arr, d, timestamp, i):

    item = arr[i]
    for key, value in d.iteritems():

        if "Item" in key:

            name = key.replace('Item', '')
            version = name+"Versions"

            if name == item:

                for versions in range(0, len(value[version])):

                    for k, v in value[version][versions].iteritems():

                        if k == 'timestamp' and checkOverlap2(v, timestamp):

                            if i+1 == len(arr):

                                dict1 = {key: value}
                                arrr.append(dict1)

                            else:

                                timeslice(arr, value[version][versions]['data'][item], timestamp, i+1)
    return arrr


items = ['specimen', 'colloquial']

arrr = []
timestamp = "2015-2015"


slices = timeslice(items, data, timestamp, 0)


item = items[-1]+'Item'
version = items[-1]+'Versions'

for i in range(0, len(slices)):
    for j in slices[i][item][version]:
        if checkOverlap2(j['timestamp'], timestamp):
            tslice = j
            original_timestamp = j['timestamp']


mydict.update({item: {"timestamp": original_timestamp, version: [tslice]}})


print mydict
#
# with open('TESTtimeslice.json', 'w') as fp:
#     json.dump(mydict, fp)



