import numpy as np
import pandas as pd

def simulate_Black_Scholes(S0, mu, sigma, T, dt) -> pd.DataFrame:
    # SIMULATE_BLACK_SHOLES calculates a temporal series of stock prices using the Black Scholes log normal model and the generated Brownian motion
    # stock_price_simulation = simulate_Black_Scholes(S0, mu, sigma, T, dt)
    #
    # Arguments:
    #   S0    = integer, specifying the initial value of the underlying asset
    #   mu    = float, specifying the drift rate of the underlying asset 
    #   sigma = float, standard deviation of the underlying asset's return
    #   T     = integer, specifying the maximum modeling time. ex. if T = 2 then modelling time will run from 0 to 2
    #   dt    = float, specifying the length of each subinterval. ex. dt=10, then there will be 10 intervals of length 0.1 between two integers of modeling time 
    #
    # Returns:
    #   stock_price_simulation = N x 2 pandas DataFrame where index is modeling time and values are a realisation of the uderlying's price
    #
    # Example:
    #   Model the price of a stock whitch is worth today 100. The market has a future annualized risk free rate of 5% and an annualized volatility of 30%. The user is interested in a price projection for the next 10 years in increments of 6 months (0.5 years)
    #   import pandas as pd
    #   import numpy as np
    #   simulate_Black_Scholes(100, 0.05, 0.3, 10, 0.5)   
    #   [out] = Time    Stock Price                
    #       0.0    100.000000
    #       0.5    131.721286
    #       1.0    124.924654
    #       1.5    209.302935
    #       2.0    222.085955
    #       2.5    208.085678
    #       3.0    165.550253
    #       3.5    239.512165
    #       4.0    176.886669
    #       4.5    148.687363
    #       5.0    181.235262
    #       5.5    164.280753
    #       6.0    172.861576
    #       6.5    170.698562
    #       7.0    141.613940
    #       7.5    121.070316
    #       8.0    116.508183
    #       8.5    104.524616
    #       9.0    146.124924
    #       9.5    202.368581
    #       10.0   262.282989
    # For more information see https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model
    
    N = int(T / dt) # number of subintervals of length 1/dt between 0 and max modeling time T

    time, delta_t = np.linspace(0, T, num = N+1, retstep = True)
    
    S = np.exp((mu - sigma ** 2 / 2) * dt + sigma * np.random.normal(0, np.sqrt(dt), size= N))
    S = np.hstack([1, S])
    S = S0* S.cumprod(axis=0)

    dict = {'Time' : time, 'Stock Price' : S}

    stock_price_simulation = pd.DataFrame.from_dict(data = dict)
    stock_price_simulation.set_index('Time', inplace = True)

    return stock_price_simulation
