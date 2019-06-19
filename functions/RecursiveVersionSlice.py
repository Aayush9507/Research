import json

with open("/Users/mymac/Documents/GitHub/Research/jsons/tjson2.json", "r") as read_file:
    data = json.load(read_file)

mydict = {}


def checkOverlap2(json1, json2):

    startA, endA = json1.split('-')
    startB, endB = json2.split('-')

    if (startA == startB) or (startB < startA <= endB) or (startB>startA and endA == endB) or endB<endA and startB > startA:
        return True
    else:

        return False


def versionslice(arr, d, i):

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
                                    arrr.append(dict1)
                                    flags[t] = 'True'

                            else:

                                versionslice(arr, versions['data'][item], i+1)
    return arrr


items = ['specimen']
ver = 1

item = items[-1]+'Item'
version = items[-1]+'Versions'

arrr = []
versionArray = []
flags = {}
flags2 = {}

slices = versionslice(items, data, 0)


# print slices

for dict in slices:
    for arrays in dict[item][version]:
        # print arrays
        t = arrays['timestamp']
        if t not in flags2 or flags2[t] == 'False':


            versionArray.append(arrays)
            flags2[t] = 'True'



slicedict = {}


timestamp = versionArray[0]['timestamp']
vslice = versionArray[0]

slicedict.update({"specimenItem": {"timestamp": timestamp, "specimenVersions": [vslice]}})


print slicedict

with open('TestVersionSlice.json', 'w') as fp:
    json.dump(slicedict, fp)




#
# for i in range(0, len(slices)):
#     for j in slices[i][item][version]:
#         if checkOverlap2(j['timestamp'], timestamp):
#             tslice = j
#             original_timestamp = j['timestamp']
#
#
# mydict.update({item: {"timestamp": original_timestamp, version: [tslice]}})
#
#
# print mydict
#
# with open('TESTtimeslice.json', 'w') as fp:
#     json.dump(mydict, fp)



