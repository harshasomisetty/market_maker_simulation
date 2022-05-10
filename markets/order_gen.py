import pandas as pd
import numpy as np
import random

def gen_orders(price, time, order_book, buy=True):
    if buy:
        offset = (1-random.uniform(0, .1))
    else:
        offset = (1+random.uniform(0, .1))
    
    price_center = price * offset
    
    num_of_orders = random.randint(2, 20)
    price_variance = .03*price_center

    
    order_prices = np.round(np.random.normal(loc=price_center, scale = price_variance, size=num_of_orders), 1)

    order_sizes = np.round(np.random.uniform(low=1, high=5, size=num_of_orders))

    final_orders = [[order_prices[i], order_sizes[i], time, 0] for i in range(num_of_orders)]

    temp_book = pd.DataFrame(final_orders, columns = ['Price', 'Size', 'Time', "MM"])
    
    return pd.concat([order_book, temp_book]).sort_values(by=['Price', 'Time'], ascending=[False, True]).reset_index(drop=True)


def gen_limit_orders(price, time, buy_book, sell_book):
    buy_book = gen_orders(price, time, buy_book)
    sell_book = gen_orders(price, time, sell_book, False)
    
    # TODO fix orderbook limits
# problem is the limit orders are overlapping, i don't now if i should fix this in greater market correction, or in same step'

    return buy_book, sell_book
