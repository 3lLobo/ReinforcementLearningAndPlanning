import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


runs = 10
# Seaborn plot uncertainty
data = pd.read_csv('./data/demand_time0.csv')
for n in range(1,runs):
    data2 = pd.read_csv('./data/demand_time%d.csv' % n)

    data = pd.concat([data, data2])
data['Timestep'] = data.index
smooth_demand = []
smooth_time = []
smooth_df = data

sm = 10
for n in range(1000*runs):
    if n % sm == 0:
        print(n)
        smooth_df[n*sm:(n+1)*sm] = data["Demand"][n*sm:(n+1)*sm].mean()

smooth_df = smooth_df[smooth_df.index % sm == 0]
ax = sns.lineplot(x="Timestep", y="Demand", data=smooth_df)
plt.show()