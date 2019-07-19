import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv


ax = plt.gca()
df = pd.read_csv("/Users/mymac/Documents/GitHub/Research/Plot_data/VersionSnapshot_ParentChange_SizeVsTime.csv")


df.plot(kind='line', x='size', y='time', ax=ax)

# plt.xticks(np.arange(min(df['size']), max(df['size']+1), 100))
# plt.yticks(np.arange(min(df['small']), max(df['large']+1), 15))

plt.ylabel("Time (Seconds) ")
plt.xlabel("Size (Kbs)")

plt.grid()
plt.savefig('VersionSnapshot_ParentChange_SizeVsTime')
plt.title('Version Snapshot Parent Change Size Vs Time')
plt.show()
