import pyrebase
from config import Config1

c1 = Config1()

firebase = pyrebase.initialize_app(c1.giveConfig())

db = firebase.database()
'''
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
'''
r_ids = db.child("schools").child("NdZ8jxVK2pSn21zeuK8ECusHoVg2").child("resources").get().val()

r_ids = list(r_ids)

'''db.child("scheduling").child("resource").child().child(r_ids[0]).push({
    "rid": r_ids[0],
    "start": "1",
    "end": "3"
    }) '''


keys = list(db.child("schools").child("NdZ8jxVK2pSn21zeuK8ECusHoVg2").child("resources").shallow().get().val())
data = []
l = 0
dat = db.child("scheduling").child("resource").child().child(keys[0]).get().val()
print(dat)
'''for i in keys:
    if l==1:
        dat = db.child("scheduling").child("resource").child(i).get().val()
        data.append(dat['end'])
    l+=1
print(data)
'''






