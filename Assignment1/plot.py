import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

labels = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
runs = 10
for n in range(runs):
    data = pd.read_csv('./data/Vgrid_%d.csv' % n)

    ax = sns.heatmap(data, robust=True)
    plt.savefig('./plots/Valueheatmap%d.png' % n)
    plt.close()