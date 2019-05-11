import json
import simplejson
from pprint import pprint
import os
from collections import namedtuple

with open('/Users/mymac/Downloads/sample.json') as f:

    x = json.load(f, object_hook=lambda d: namedtuple('foo', d.keys())(*d.values()))
    # x = json.load(f)

print x
# print x[1].__dict__

# print hasattr(x[1].id, 'oid')
try:
    print x[1]

except AttributeError:
    print " attribute err"











#
# with open('/Users/mymac/Downloads/example_2.json') as f:
#     data = json.load(f)
#
# pprint(data)

# dirname = '/Users/mymac/Downloads/'
#
# filename = 'example_2.json'
#
# with open(os.path.join(dirname, filename)) as fd:
#     json_data = simplejson.loads(fd.decode("utf-8"))