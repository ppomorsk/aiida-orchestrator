"""
Test program to see if logs read correctly"
"""



import json

f=open("/home/ubuntu/computers/computers_aiida.json","r")
g=f.readlines()
f.close()

computers=json.loads(g[0])
computer_list=[]
for d in computers:
     computer_list.append(d["computer"])


fairshare_list=[]
for cluster in computer_list:

    f=open("/home/ubuntu/computers/"+cluster+".load.log","r")
    g=f.readlines()
    f.close()
    last=g[-1].split(",")
    fairshare_list.append(last[1]) 

maxfairshare=fairshare_list.index(max(fairshare_list))
cluster_with_max_fairshare=computer_list[maxfairshare]
print(cluster_with_max_fairshare)
