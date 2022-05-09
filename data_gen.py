import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
# https://towardsdatascience.com/how-to-simulate-a-stock-market-with-less-than-10-lines-of-python-code-5de9336114e5
np.random.seed(0)
mu = 0.001
sigma = 0.01
start_price = 5
periods = 1000



def gen_price_series():
    
    returns = np.random.normal(loc=mu, scale=sigma, size=periods)
    return start_price*(1+returns).cumprod()

def gen_buy_orders(price, time, buy_book):
#      1) random size
#      2) for buys normal distribution centered around a uniform distribution mean diff between fair price
#      3) similar for sells norm dist around uniform dist
#      4) some random amount of market orders (low or high volume)
    offset = (1-random.uniform(0, .1))
    price_center = price * offset
    
    num_of_orders = random.randint(2, 20)
    price_variance = .03*price_center

    
    order_prices = np.round(np.random.normal(loc=price_center, scale = price_variance, size=num_of_orders), 1)

    order_sizes = np.round(np.random.uniform(low=1, high=5, size=num_of_orders))

    final_orders = [[order_prices[i], order_sizes[i], time, False] for i in range(num_of_orders)]

    temp_buy_book = pd.DataFrame(final_orders, columns = ['Price', 'Size', 'Time', "MM"])
    
    # print(sorted(order_prices))
    # print(price, offset, price_center, num_of_orders)
    # print(temp_buy_book)
    
    return pd.concat([buy_book, temp_buy_book]).sort_values(by=['Price', 'Time'], ascending=[False, True])

def mm1_move():
#      1) the market gives feedback to the mm which provides more liquidity (more of its orders are filled)
#      2) mms assume that last mm will keep same strategy
    return

def market_sim():
    #   1) underlying price
    price_series = gen_price_series()
    
    buy_book = pd.DataFrame(columns = ['Price', 'Size', 'Time', "MM"])
    sell_book = pd.DataFrame(columns = ['Price', 'Size', 'Time', "MM"])
    
    
    buy_book = gen_buy_orders(start_price, 0, buy_book)
    print("final buy book", buy_book)
    for time, price in enumerate(price_series[:1], 1):
        print("time", time)
        #   2) mm order placement
        # mm1_move()
        
        #   3) generate random orders around price, random volume
        buy_book = gen_buy_orders(price, time, buy_book)

        print(buy_book)
        # sell_orders = gen_sell_orders(price)

        #   4) cancel some orders

        
        
    
# plt.plot(price)
# plt.show()


if __name__ == "__main__":
    market_sim()










# market steps
# 1) read market price, who provided most liquidity last round
# 2) mm1 change orders
# 3) mm2 change orders
# 4) market orders come in
# 5) store edge for each mm, market input on which mm gave more liq, repeat
