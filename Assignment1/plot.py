import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('Ogrid_8.csv')
ax = sns.heatmap(data)
plt.show()