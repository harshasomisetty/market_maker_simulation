import pandas as pd

def mm_move(mm, price, time, buy_book, sell_book, redo_orders = False, reward = 0):
    # print("mm move")
    inven_ratio = sum(mm["inven"])/mm["max_inven"]
    price_center = price
    spread_size = None

    # print(f"\nprice_cent {price_center}, inven_ratio {inven_ratio} total: {sum(mm['inven'])}")
    if inven_ratio < .25: # If too little inventory, will move down price center to sell more
        price_center = price_center - price_center*(1-inven_ratio)/2
    elif inven_ratio > .75: # too much inventory, move up center to buy more
        price_center = price_center + price_center*(inven_ratio)/2

    if reward == 0: # mm really wants reward, will tighten spread
        spread_size = .05
    elif reward == 1: # mm got a decent reward, keeps spead
        spread_size = .1
    elif reward == 2: # Widen spread, already got reward
        spread_size = .15

    # print("MM price", price_center, spread_size, price_center*(1-spread_size))
    mm_buy = [[round(price_center*(1-spread_size), 1), mm["order_size"], time, mm["id"]]]
    temp_buy_book = pd.DataFrame(mm_buy, columns = ['Price', 'Size', 'Time', "MM"])


    mm_sell = [[round(price_center*(1+spread_size), 1), mm["order_size"], time, mm["id"]]]
    
    temp_sell_book = pd.DataFrame(mm_sell, columns = ['Price', 'Size', 'Time', "MM"])

    buy_book.drop(buy_book[buy_book.MM == mm["id"]].index, inplace = True)

    sell_book.drop(sell_book[sell_book.MM == mm["id"]].index, inplace = True)
    
    final_buy_book = pd.concat([buy_book, temp_buy_book]).sort_values(by=['Price', 'Time'], ascending=[False, True]).reset_index(drop=True)
        
    final_sell_book = pd.concat([sell_book, temp_sell_book]).sort_values(by=['Price', 'Time'], ascending=[True, True]).reset_index(drop=True)

    # print(f"MM move: price {price}, price_center {price_center}, spread {spread_size}")
    return final_buy_book, final_sell_book
