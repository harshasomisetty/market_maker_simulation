import numpy as np
import pandas as pd
import random


# https://towardsdatascience.com/how-to-simulate-a-stock-market-with-less-than-10-lines-of-python-code-5de9336114e5

def gen_price_series(mu, sigma, periods, start_price):
    
    returns = np.random.normal(loc=mu, scale=sigma, size=periods)
    return start_price*(1+returns).cumprod()

def FIFO_matching():
    # calculate edge, subtract edge for too much inventory
    return


def cancel_trades(book):
    frac_to_drop = random.uniform(.4, .5)
    remove_n = int(frac_to_drop*len(book.index))
    
    drop_indices = np.random.choice(book.index, remove_n, replace=False)
    return book.drop(drop_indices)
    
def gen_market_move(buy_book, sell_book):

    # for market orders, just generate random quantity (either large or small), and then fifo that to the orderbook

    # 3) Store edge for market makers
    

    print("before: ", len(buy_book.index), len(sell_book.index))
    
    buy_book, sell_book = cancel_trades(buy_book), cancel_trades(sell_book)

    print("after: ", len(buy_book.index), len(sell_book.index))
    
    return buy_book, sell_book
    
