#!/usr/bin/env python
# coding: utf-8


import numpy as np
from BinomialTreeOption import BinomialOption


class BinomialLROption(BinomialOption):

    def setup_parameters(self):
        
        odd_N = self.N if (self.N % 2 == 1) else (self.N + 1)
        d1 = (np.log(self.S0 / self.K) + ((self.r - self.div) +
                                          self.sigma ** 2 / 2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = (np.log(self.S0 / self.K) + ((self.r - self.div) -
                                          self.sigma ** 2 / 2) * self.T) / (self.sigma * np.sqrt(self.T))
        
        def pp_2_inversion(z, n): return 0.5 + np.copysign(1, z) * np.sqrt(
            0.25 - 0.25 * np.exp(-((z / (n + 1 / 3 + 0.1/(n + 1))) ** 2) * (n + 1/6)))
                                                                            
        pbar = pp_2_inversion(d1, odd_N)

        self.p = pp_2_inversion(d2, odd_N)
        # self.df is the discount factor
        self.u = 1 / self.df * (pbar / self.p)
        self.d = (1 / self.df - self.p * self.u) / (1 - self.p)
        self.qu = self.p
        self.qd = 1 - self.p

def main():

    eu_option = BinomialLROption(50, 50, 0.05, 0.5, 3, {'sigma':0.3, 'is_call':False})
    print("European Option: %s" % eu_option.price())

    am_option = BinomialLROption(50, 50, 0.05, 0.5, 3, {'sigma':0.3, 'is_call':False, 'is_eu':False})
    print("American Option: %s" % am_option.price())


if __name__ == '__main__':
    main()