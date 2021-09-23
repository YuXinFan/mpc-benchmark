import pandas as pd 

p0=pd.read_csv("Party-0.csv", header=0,names=['Name', 'InSize', 'Type', 'Val', "Repeat"])
p1=pd.read_csv("Party-1.csv", header=0)
print(p0)

for i in range(len(p0["Val"])):
    p0["Val"][i] = max(p0["Val"][i],p1["Val"][i])
