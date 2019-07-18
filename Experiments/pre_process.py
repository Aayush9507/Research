import json
import os.path
import random
path = '/Users/mymac/Documents/GitHub/Research/Experiments/parent_change/parent_change_folder_medium'


for file in os.listdir(path):

    full_filename = "%s/%s" % (path, file)

    with open(full_filename, "r") as read_file:

        year_count = 1200

        data = json.load(read_file)

        for file in data:

            year_count += 1

            file['timestamp'] = unicode(year_count)+'-'+unicode(year_count)

            if 'subname' in file['data']['specimen']:
                file['data']['specimen']['subname'+str(year_count)] = file['data']['specimen']['subname']

                del file['data']['specimen']['subname']

            with open(full_filename, 'w') as fp:
                json.dump(data, fp)
