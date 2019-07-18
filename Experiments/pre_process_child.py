import json
import os.path

path = '/Users/mymac/Documents/GitHub/Research/Experiments/child_change_folder_small'


for file in os.listdir(path):

    full_filename = "%s/%s" % (path, file)

    with open(full_filename, "r") as read_file:

        year_count = 1200

        data = json.load(read_file)

        for file in data:

            year_count += 1

            file['timestamp'] = unicode(year_count)+'-'+unicode(year_count)

            with open(full_filename, 'w') as fp:
                json.dump(data, fp)