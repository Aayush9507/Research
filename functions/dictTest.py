

d={
    "name":"aayush",
    "address":"Darwin"
}

d2={}
d2.update({"data":{"specimen":{}}})

print d2

for k, v in d.iteritems():
    # print k, v

    d2['data']['specimen'].update({k: v})

print d2





