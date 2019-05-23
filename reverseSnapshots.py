import json

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
    pjson.update({"specimenItem": {"timestamp": "", "specimenVersions": []}})

    for i in range(0, len(keylist)):
        pjson['specimenItem']['specimenVersions'].append({})

    arr=[]
    for j in keylist:

        vdict={}
        vdict.update({"timestamp":"", 'data': {'specimen':{}}})
        for k in j:
            itemname = k+'Item'
            num = 0
            while num < len(keylist):

                vdict["data"]["specimen"].update({itemname: ''})
                num = num+1

        arr.append(vdict)

    pjson['specimenItem']['specimenVersions']=arr

    print "new pjson is: ", pjson

    with open('reversedJson.json', 'w') as fp:
        json.dump(pjson, fp)





























keylist = get_keylist(data)

create_skeleton(keylist)
