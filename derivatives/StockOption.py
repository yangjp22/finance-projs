#!/usr/bin/env python
# coding: utf-8

import numpy as np

# Store common attributions of a stock option
  
class StockOption(object):
    
    def __init__(self, S0, K, r, T, N, params):
        self.S0 = S0
        self.K = K
        self.r = r
        self.T = T
        self.N = np.max([1, N]) # Ensure N have at least 1 time step
        self.STs = None # Declare the stock prices tree
        
        # Optional parameters used by derived classes
        self.pu = params.get("pu", 0) # Probability of up state
        self.pd = params.get("pd", 0)  # Probability of down state
        self.div = params.get("div", 0) # Dividend yield
        self.sigma = params.get("sigma", 0) # Volatility
        self.is_call = params.get("is_call", True) # Call or Put, default is Call
        self.is_european = params.get("is_eu", True) # European or American, default is European
        
        self.dt = T / float(N)  # Single time step, in years
        self.df = np.exp(-(r - self.div) * self.dt) # Discount factor

