import numpy as np
import pandas as pd
import random


# https://towardsdatascience.com/how-to-simulate-a-stock-market-with-less-than-10-lines-of-python-code-5de9336114e5

def gen_price_series(mu, sigma, periods, start_price):
    
    returns = np.random.normal(loc=mu, scale=sigma, size=periods)
    return start_price*(1+returns).cumprod()


def cancel_trades(book):
    remove_n = int(random.uniform(.4, .5)*len(book.index))
    
    mm_indexes = book[(book.MM.isin([1, 2]))].index

    drop_indices = np.random.choice(book.index, remove_n, replace=False)

    final_drop = np.delete(drop_indices, np.argwhere(np.isin(drop_indices, mm_indexes)))

    return book.drop(final_drop).reset_index(drop=True)
    
def gen_market_move(buy_book, sell_book, mm1, mm2, price):
    
    def execute_fifo_orders(book):
        trade_quant = random.randint(10, 20)
        # print("book", book)
        print("trade quant", trade_quant)
        for index, row in book.iterrows():
            if trade_quant > 0:
                cur_size = row["Size"]

                quant_fulfilled = 0
  
                if trade_quant >= cur_size:
                    trade_quant -= cur_size
                    print("new quant", trade_quant, "dropping index", index)
                    quant_fulfilled = cur_size
                    book.drop(index, inplace=True)
                else:
                    print(f"changing {cur_size} by {trade_quant}. index: {index}")
                    
                    remaining_size = cur_size - trade_quant
                    trade_quant = 0
                    quant_fulfilled = row["Size"] - remaining_size
                    book.at[index, "Size"] = remaining_size

                    
                # MM Moves recalcing edge
                if row["MM"] == 1:
                    print("IS MM 1 ORDER")
                    mm1["edge"].append(quant_fulfilled*abs(row["Price"] - price))
                elif row["MM"] == 2:
                    mm2["edge"].append(quant_fulfilled*abs(row["Price"] - price))
                    print("IS MM 2 ORDER")                  
            else:
                break
            
        print(f"MM1 EDGE {mm1['edge']} and mm2 {mm1['edge']}")

        return book

    # TODO make this low volume or high volume randomly


    # SELL BOOK, need to reverse to properly do fifo
    sell_book = sell_book.loc[::-1].reset_index(drop=True)
    sell_book = execute_fifo_orders(sell_book)
    sell_book = sell_book.loc[::-1].reset_index(drop=True)

    # BUY BOOK
    # print("pre loop\n", buy_book)
    buy_book = execute_fifo_orders(buy_book)
    # print("post loop\n", buy_book)
    
    # remember which orders are filled by MMs
    

    
    buy_book, sell_book = cancel_trades(buy_book), cancel_trades(sell_book)

    return buy_book, sell_book
    
