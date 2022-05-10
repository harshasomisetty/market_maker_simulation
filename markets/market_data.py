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
    remove_n = int(random.uniform(.4, .5)*len(book.index))
    
    mm_indexes = book[(book.MM.isin([1, 2]))].index

    drop_indices = np.random.choice(book.index, remove_n, replace=False)

    final_drop = np.delete(drop_indices, np.argwhere(np.isin(drop_indices, mm_indexes)))

    return book.drop(final_drop).reset_index(drop=True)
    
def gen_market_move(buy_book, sell_book, mm1, mm2):

    # TODO make this low volume or high volume randomly
    buy_quant, sell_quant = random.randint(0, 9), random.randint(0, 9)

    
    # fifo clear buys and sells

    # remember which orders are filled by MMs
    

    
    buy_book, sell_book = cancel_trades(buy_book), cancel_trades(sell_book)

    return buy_book, sell_book
    
