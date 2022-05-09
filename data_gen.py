import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# https://towardsdatascience.com/how-to-simulate-a-stock-market-with-less-than-10-lines-of-python-code-5de9336114e5
np.random.seed(0)

def gen_price_series():
    mu = 0.001
    sigma = 0.01
    start_price = 5
    periods = 1000

    returns = np.random.normal(loc=mu, scale=sigma, size=periods)
    return start_price*(1+returns).cumprod()

def gen_orders():
    price_series = gen_price_series()
    # print(price_series)
    
    num_of_orders = randint(0, 100)
    price = 
    size

    
    
# plt.plot(price)
# plt.show()


if __name__ == "__main__":
    gen_orders()


