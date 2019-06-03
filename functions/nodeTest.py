class Node:

    def __init__(self, t, k, v, ts):

        self.t = t
        self.k = k
        self.v = v
        self.ts = ts


    def display (self):

        print("t: %s \nk: %s \nv %s \nts %s"%(self.t, self.k, self.v, self.ts))


arr=[]

n1 = Node("unicode", "name", "Hieracium umbellatum", "2015-2015")

arr.append(n1)

n1 = Node("list", "aayush", "Canadian Hawkweed", "2016-2018")

arr.append(n1)




# print arr

for i in range(0, len(arr)):
    print arr[i].display()