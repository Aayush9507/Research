import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
import seaborn as sns


ax = plt.gca()
df = pd.read_csv("/Users/mymac/Documents/GitHub/Research/Plot_data/reversing_json_child_change.csv")


df.plot(kind='line', x='file_size', y='time', ax=ax, color='green')


# plt.xticks(np.arange(min(df['changes']), max(df['changes']+1), 100))
# plt.yticks(np.arange(min(df['small']), max(df['large']+1), 15))

plt.ylabel("Time (seconds)")
plt.xlabel("Size (KB)")
# plt.title('Document Creation Size Vs Time ( Parent Version Changes )')
plt.grid()
plt.tight_layout()

plt.savefig('/Users/mymac/Documents/GitHub/Research/Experiments/plot_images/ChangesVsTime/Document_Creation_Child_Change.png')
plt.show()
