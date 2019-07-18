import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv


ax = plt.gca()
df = pd.read_csv("/Users/mymac/Documents/GitHub/Research/Plot_data/Version_snapshot_ParentChange.csv")


df.plot(kind='line', x='changes', y='small', ax=ax)
df.plot(kind='line', x='changes', y='medium', ax=ax)
df.plot(kind='line', x='changes', y='large', ax=ax)

plt.xticks(np.arange(min(df['changes']), max(df['changes']+1), 100))
# plt.yticks(np.arange(min(df['small']), max(df['large']+1), 15))

plt.ylabel("Time (Seconds) ")
plt.xlabel("Changes (Key-Value Pairs)")

plt.grid()
plt.savefig('VersionSnapshot_Parent_Version_Change_Plot')
plt.title('VersionSnapshot Parent Version Change Plot')
plt.show()
