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

def main():

    ''' The grid will store the values for all possible states. '''
    value_grid = np.zeros((steps, M))
    demand_list = np.zeros(steps)

    ''' Loop over all timesteps and x values. '''
    print('Start simulation!')
    for t in range(steps-2, 0, -1):
        for x in range(M):
            demand_prob = 1/t
            demand_t = np.random.choice([demand, 0], 1, [demand_prob, 1-demand_prob])
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
            v = k * n_order + value_grid[t+1, x-demand_t+n_order]
            min_idx = np.argmin(v)
            value_grid[t] = v[min_idx]
    print('Done!')
    print(value_grid)
    df = pd.DataFrame() 
    for n in range(steps):
        df['inventory' + str(n)] = value_grid[:,n]
    df.to_csv()
if __name__ == "__main__":
    main()