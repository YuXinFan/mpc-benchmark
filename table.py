import pandas as pd 

p0=pd.read_csv("Party-0.csv", names=['Name', 'InSize', 'Type', 'Val', "Repeat"])
p1=pd.read_csv("Party-1.csv", names=['Name', 'InSize', 'Type', 'Val', "Repeat"])
pp ={"Name": p0["Name"], "InSize": p0["InSize"],"Type": p0["Type"]}
val = []
l0 = p0["Val"].to_list()
l1 = p1["Val"].to_list()
assert(len(l0)==len(l1))
for i in range(len(l0)):
    v1 = l0[i]
    v2 = l1[i]
    val.append(max(v1,v2))
pp["Val"] = val 
pp["Repeat"] = p0["Repeat"]
df = pd.DataFrame(pp)
df.to_csv("./Party.csv", index=False)
print(df)
