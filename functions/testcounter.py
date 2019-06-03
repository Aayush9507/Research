import collections


l1 = ['colloquial', 'habitat', 'name']
l2 = ['colloquial', 'habitat']
l3 = ['aayush', 'colloquial', 'habitat']

l4 = ['aayush', 'colloquial', 'habitat']

l5 = ['aayush', 'habitat', 'colloquial']







if collections.Counter(l5) == collections.Counter(l4):
    print ("identical")

else:
    print "not identical"



