from collections import namedtuple
import simplejson


with open('tjson.json') as f:
    json = simplejson.load(f, object_hook=lambda d: namedtuple('foo', d.keys())(*d.values()))


for key, value in json:
    for k,v in value:
        print k,v