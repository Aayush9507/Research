import json
with open("jsons/recur_json.json", "r") as read_file:
    data = json.load(read_file)


def checkOverlap(json1, json2):

    startA, endA = json1.split('-')
    startB, endB = json2.split('-')

    if (startA == startB) or (startB < startA <= endB):
        return True
    else:
        return False

# def give_recursive_items(d, item, t):
#
#     for key, value in d.iteritems():
#
#         if "Item" in key:
#             # print k1
#             name = key.replace('Item', '')
#             version = name+"Versions"
#
#             if name == item:
#                 for versions in value[version]:
#
#                     for k, v in versions.iteritems():
#                         if k == 'timestamp' and v == t:
#                             return versions['data'][item]


def give_recursive_items2(arr, d, i, t):

    item = arr[i]
    for key, value in d.iteritems():
        # print key,value

        if "Item" in key:
            # print k1
            name = key.replace('Item', '')
            version = name+"Versions"

            if name == item:
                for versions in value[version]:

                    for k, v in versions.iteritems():
                        # print k, v
                        # print t, v
                        if k == 'timestamp' and checkOverlap(t, str(v)) == True:
                            if i+1 == len(arr):
                                dict1 = {key:''}

                                dict1[key]=value
                                return dict1


                            else:
                                return give_recursive_items2(arr, versions['data'][item], i+1, t)


arr = ['specimen', 'name']
t = '2016-2018'

print "one...", give_recursive_items2(arr, data, 0, t)



# print data

# for i in range(0,  len(arr)):
#     item = arr[i]
#
#     data = give_recursive_items(data, item, t)
#
#     print item, ".......", data

# print data


# # print ndata
#
# for i in range(1, len(arr)):
#     item = arr[i]
#     print "item is...", item
#     itemdata = give_recursive_items(ndata, item, t)
#
#     print itemdata
#
#
# print itemdata
#
