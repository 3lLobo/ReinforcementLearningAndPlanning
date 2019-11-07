import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

''' Loop over all runs and find the optimal policy for each. 
    Plot them over time and include demand and order count. '''
for run in range(10):
    p_df = pd.read_csv('./data/Pgrid_%d.csv' % run)
    p_data = p_df.to_numpy()[:,1:]
    o_df = pd.read_csv('./data/Ogrid_%d.csv' % run)
    o_data = o_df.to_numpy()[:,1:]
    d_df = pd.read_csv('./data/demand_time%d.csv' % run)
    demand = d_df.to_numpy()[:,1]

    ''' Get max Profit and track the inventory path.
        We use armax to get the index of the maximum profit in a row. '''
    print(p_data.shape)
    max_idx  = np.argmax(p_data[1,:])
    print("Starting invantory size for max profit:", max_idx)

    # Init empty arrays
    inv_array = np.zeros(1000)
    order_array = np.zeros(1000)
    order_n = o_data[0, max_idx]
    demand_array = np.zeros(1000)
    demand_array[0] = demand[0]
    inv_array[0] = max_idx - demand[0] 

    # Loop over all timesteps and track the optimal policy
    order_array[0] = order_n
    idx = max_idx
    for n in range(1,1000):
        idx =  int(idx + order_n)
        order_n = o_data[n, idx]
        inv_array[n] = inv_array[n-1] - demand[n]
        order_array[n] = order_array[n] + order_n
        demand_array[n] = demand_array[n-1] + demand[n]
        
    # It follow an overcomplicated code to prepare the data for a plot
    time_array = np.linspace(0,1000, num=1000, dtype=int)

    df_order = pd.DataFrame()
    df_order['Amount'] = order_array
    df_order['Timesteps'] = time_array
    df_order['Feature'] = ["Order"]*1000

    df_inv = pd.DataFrame()
    df_inv['Amount'] = inv_array
    df_inv['Timesteps'] = time_array
    df_inv['Feature'] = ["Inventory"]*1000

    df_demand = pd.DataFrame()
    df_demand['Amount'] = demand_array
    df_demand['Timesteps'] = time_array
    df_demand['Feature'] = ["Demand"]*1000

    # We concatenate the data to fit it in one plot
    if run == 0:
        df_plot = pd.concat([df_inv, df_order, df_demand])
    else:
        df_plot2 = pd.concat([df_inv, df_order, df_demand])
        df_plot = pd.concat([df_plot, df_plot2])

# We create a beautiful plot <3     
sns.lineplot(x='Timesteps', y='Amount', hue='Feature', data=df_plot)
plt.show()
