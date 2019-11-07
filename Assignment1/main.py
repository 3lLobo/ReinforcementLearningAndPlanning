import numpy as np
import pandas as pd
import seaborn as sns

''' Parameter setting '''
steps = 1000
demand = 1
sell_price = 20
purch_price = 10
order_limit = 900
M = steps               # Assuming the max of one demand per time step
runs = 10
seed = 6                # Set random seed for reproducability

def main():

    ''' The grid will store the values for all possible states. '''
    value_grid = np.zeros((steps, M))
    profit_grid = np.zeros((steps, M))
    order_grid = np.zeros((steps, M))
    demand_list = np.zeros(steps)
    for run in range(runs):

        ''' Loop over all timesteps and x values. '''
        np.random.seed( seed+run )
        print('Start simulation! Run %d' % run)
        for t in range(steps-1, 0, -1):
            for x in range(M):
                demand_prob = (t+1)/steps
                print(demand_prob)
                demand_t = np.random.choice([demand, 0], 1, p=[demand_prob, 1-demand_prob])
                print(demand_t) 
                demand_list[t] = demand_t
                if t > 500:
                    k = purch_price + 5
                elif t > 900:
                    k = 100000
                else:
                    k = purch_price
                if demand > x:
                    n_order = np.linspace(demand_t-x, M-x+demand_t, M, dtype=int, endpoint=False)
                else:
                    n_order = np.linspace(0, M-x+demand_t, M-x+demand_t, dtype=int, endpoint=False)
                if t == 999:
                    #v = x * purch_price
                    p = demand_t * sell_price - x * purch_price
                    p_order = 0
                else:
                    p = demand_t * sell_price - n_order * k + profit_grid[t+1, x-demand_t+n_order]
                    max_idx = np.argmax(p)
                    p = p[max_idx]
                    p_order = n_order[max_idx]
                    #v = k * n_order + value_grid[t+1, x-demand_t+n_order]
                    #min_idx = np.argmin(v)
                    #v = v[min_idx]
                    #p = n_order[min_idx] * sell_price - v + profit_grid[t+1, x-demand_t+n_order[min_idx]]
                print('p', p)
                #value_grid[t,x] = v
                profit_grid[t,x] = p
                order_grid[t,x] = p_order
            demand_list[t] = demand_t

        ''' Save Data as cvs file.'''
        print('Saving ...')
        #df = pd.DataFrame() 
        df2 = pd.DataFrame()
        df_order = pd.DataFrame()
        df_demand = pd.DataFrame()
        df_demand['Demand'] = demand_list 
        for n in range(steps):
            #df['inventory' + str(n)] = value_grid[:,n]
            df2['inventory' + str(n)] = profit_grid[:,n]
            df_order['inventory' + str(n)] = order_grid[:,n]
        #df.to_csv('Vgrid_%d.csv' % run)
        df2.to_csv('Pgrid_%d.csv' % run)
        df_order.to_csv('Ogrid_%d.csv' % run)
        df_demand.to_csv("demand_time%d.csv" % run)
        print('Done!')


if __name__ == "__main__":
    main()