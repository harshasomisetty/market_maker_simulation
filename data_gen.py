import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

from markets.order_gen import gen_limit_orders
from markets.maker_moves import mm_move
from markets.market_data import gen_price_series, gen_market_move

np.random.seed(0)
mu = 0.001
sigma = 0.01
start_price = 5
periods = 1000

mm1 = {"edge": 0, "inven": 15, "max_inven": 30, "order_size": 5, "id": 1}
mm2 = {"edge": 0, "inven": 5, "max_inven": 15, "order_size": 3, "id": 2}


def market_sim():
    price_series = gen_price_series(mu, sigma, periods, start_price)
    
    buy_book = pd.DataFrame(columns = ['Price', 'Size', 'Time', "MM"])
    sell_book = pd.DataFrame(columns = ['Price', 'Size', 'Time', "MM"])

    buy_book, sell_book = mm_move(mm1, start_price, 0, buy_book, sell_book, False, 0)
    buy_book, sell_book = mm_move(mm2, start_price, 0, buy_book, sell_book, False, 0)
    
    buy_book, sell_book = gen_limit_orders(start_price, 0, buy_book, sell_book)
    
    print("time 0 price", start_price)
    print("final sell book", sell_book)
    print("final buy book", buy_book)
    
    for time, price in enumerate(price_series[:2], 1):
        print("\n\nnext step: time", time, "price", price, "\n\n")

        # TODO change reward

        buy_book, sell_book = mm_move(mm1, price, time, buy_book, sell_book, True, 0)

        buy_book, sell_book = mm_move(mm2, price, time, buy_book, sell_book, True, 0)

        buy_book, sell_book = gen_limit_orders(price, time, buy_book, sell_book)

        buy_book, sell_book = gen_market_move(buy_book, sell_book, mm1, mm2)

        print("final sell book\n", sell_book)
        print("final buy book\n", buy_book)


if __name__ == "__main__":
    market_sim()
