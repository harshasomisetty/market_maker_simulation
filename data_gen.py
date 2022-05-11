import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

from markets.order_gen import gen_limit_orders
from markets.maker_moves import mm_move
from markets.market_data import gen_price_series, gen_market_move

np.random.seed(3)
mu = 0.000
sigma = 0.02
start_price = 5
periods = 1000

def market_sim():
    mm1 = {"edge": [], "inven": [15], "max_inven": 30, "order_size": 5, "id": 1}
    mm2 = {"edge": [], "inven": [5], "max_inven": 15, "order_size": 3, "id": 2}

    vol_contributor = 0

    price_series = gen_price_series(mu, sigma, periods, start_price)
    
    buy_book = pd.DataFrame(columns = ['Price', 'Size', 'Time', "MM"])
    sell_book = pd.DataFrame(columns = ['Price', 'Size', 'Time', "MM"])

    buy_book, sell_book = mm_move(mm1, start_price, 0, buy_book, sell_book, 0)
    buy_book, sell_book = mm_move(mm2, start_price, 0, buy_book, sell_book, 0)
    
    buy_book, sell_book = gen_limit_orders(start_price, 0, buy_book, sell_book)
    
    print("time 0 price", start_price)
    print("final sell book", sell_book)
    print("final buy book", buy_book)
    
    for time, price in enumerate(price_series, 1):
        # print("\n\nnext step: time", time, "price", price, "\n\n")

        buy_book, sell_book = mm_move(mm1, price, time, buy_book, sell_book, vol_contributor)

        buy_book, sell_book = mm_move(mm2, price, time, buy_book, sell_book, 2-vol_contributor)

        buy_book, sell_book = gen_limit_orders(price, time, buy_book, sell_book)

        buy_book, sell_book, mm1, mm2, vol_contributor = gen_market_move(buy_book, sell_book, mm1, mm2, price)

        # print("final sell book\n", sell_book)
        # print("final buy book\n", buy_book)
        # print(f"final mm stats: \n{mm1} \n{mm2}")
        # print("***")

    print(f"final mm stats: \n{mm1} \n{mm2}")

    plt.plot(range(0, periods), mm1["edge"], label=f'MM1: edge {sum(mm1["edge"])}')
    plt.plot(range(0, periods), mm2["edge"], label=f'MM2: edge {sum(mm2["edge"])}')
    plt.title("Edge over time of Market Makers: Stable market")
    plt.xlabel("Market Iterations")
    plt.ylabel("Edge")
    plt.legend(loc="upper left")
    plt.show()
    
def graph_prices():
    price_series = gen_price_series(mu, sigma, periods, start_price)

    plt.plot(price_series)
    plt.show()
if __name__ == "__main__":
    market_sim()

    # graph_prices()
