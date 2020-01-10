#!/usr/local/bin/python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys 

path_to_csv= sys.argv[1] 
df= pd.read_csv(path_to_csv, index_col=False, header=None, skipinitialspace=True)
df = df.apply(pd.to_numeric, errors='coerce')
#df.apply(pd.to_numeric, errors='ignore')
#df.describe()
for col in range(20):
    df[col] = df[col].astype(int)
#print(df)
#sns.heatmap(df, fmt="d")
sns.heatmap(df,annot=True, fmt="d")
#plt.imshow(df,cmap='hot',interpolation='nearest')
plt.show()
