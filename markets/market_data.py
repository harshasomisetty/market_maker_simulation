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
        trade_quant = random.choice([5, 20])
        edges = [0,0]
        volume = [0,0]
        # print("book", book)
        # print(f"\n\ntrade quant {trade_quant}")
        for index, row in book.iterrows():
            if trade_quant > 0:
                cur_size = row["Size"]

                quant_fulfilled = 0 
  
                if trade_quant >= cur_size:
                    trade_quant -= cur_size
                    # print("new quant", trade_quant, "dropping index", index)
                    quant_fulfilled = cur_size
                    book.drop(index, inplace=True)
                else:
                    # print(f"changing {cur_size} by {trade_quant}. index: {index}")
                    remaining_size = cur_size - trade_quant
                    trade_quant = 0
                    quant_fulfilled = row["Size"] - remaining_size
                    book.at[index, "Size"] = remaining_size

                    
                # MM Moves recalcing edge
                if row["MM"] == 1:
                    # print(f"IS MM 1 ORDER: {quant_fulfilled*abs(row['Price'] - price)}")
                    edges[0] += quant_fulfilled*abs(row["Price"] - price)
                    volume[0] += quant_fulfilled
                elif row["MM"] == 2:
                    edges[1] += quant_fulfilled*abs(row["Price"] - price)
                    volume[1] += quant_fulfilled                    
                    # print(f"IS MM 2 ORDER {quant_fulfilled*abs(row['Price'] - price)}")                  
            else:
                break
            
        # print(f"final edges {edges}")
        
        return book, edges, volume

    # TODO make this low volume or high volume randomly


    # SELL BOOK, need to reverse to properly do fifo
    sell_book = sell_book.loc[::-1].reset_index(drop=True)
    sell_book, edges, sell_vol = execute_fifo_orders(sell_book)
    sell_book = sell_book.loc[::-1].reset_index(drop=True)

    # BUY BOOK
    # print("pre loop\n", buy_book)
    buy_book, edges1, buy_vol = execute_fifo_orders(buy_book)
    # print("post loop\n", buy_book)

    mm1["inven"].append(sell_vol[0] - buy_vol[0])
    mm2["inven"].append(sell_vol[1] - buy_vol[1])
    # print(f"Buys: {buy_vol} sells: {sell_vol}")
    # if true, then mm1 contributed most to volume
    vol_contributor = (sell_vol[0] + buy_vol[0]) > (sell_vol[1] + buy_vol[1])
    
    mm1["edge"].append(edges[0] + edges1[0])
    mm2["edge"].append(edges[1] + edges1[1])
    # print(f"MM1 EDGE {mm1['edge']} and mm2 {mm2['edge']}")

    # remember which orders are filled by MMs
    

    
    buy_book, sell_book = cancel_trades(buy_book), cancel_trades(sell_book)

    return buy_book, sell_book, mm1, mm2, vol_contributor
    
