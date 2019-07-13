import pyrebase
from config import Config1

c1 = Config1()

firebase = pyrebase.initialize_app(c1.giveConfig())

db = firebase.database()

cluster = db.child("clusters").shallow().get()
clus_key = cluster.val()

keyList = [i for i in list(clus_key)]
lis=[]

for i in keyList:
    clust_e = db.child("clusters").child(i).get().val()
    li1=[]
    
    li1.append(clust_e['c_name'])
    
    names = []
    for j in clust_e['schools_present']:
        x = db.child("schools").child(j).get().val()
        names.append(x['name'])
    li1.append(names)
lis.append(li1)
print(lis)







