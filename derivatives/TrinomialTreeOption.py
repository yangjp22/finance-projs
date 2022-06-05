#!/usr/bin/env python
# coding: utf-8

import numpy as np
from BinomialTreeOption import BinomialOption

class TrinomialOption(BinomialOption):

    def setup_parameters(self):
        '''Required calculations for the model '''
        self.u = np.exp(self.sigma * np.sqrt(2 * self.dt))
        self.d = 1 / self.u
        self.m = 1
        self.qu = ((np.exp((self.r - self.div) * self.dt / 2) - np.exp(-self.sigma * np.sqrt(self.dt / 2))) /
                   (np.exp(self.sigma * np.sqrt(self.dt/2)) - np.exp(-self.sigma * np.sqrt(self.dt/2)))) ** 2
        self.qd = ((np.exp(self.sigma * np.sqrt(self.dt / 2)) - np.exp((self.r - self.div) * self.dt / 2)) /
                   (np.exp(self.sigma * np.sqrt(self.dt/2)) - np.exp(-self.sigma * np.sqrt(self.dt/2)))) ** 2
        self.qm = 1 - self.qd - self.qu

    def initialize_stock_price_tree(self):
        ''' Initialize a 2D tree at t = 0 '''
        self.STs = [np.array([self.S0])]

        for i in range(self.N):
            prev_nodes = self.STs[-1]
            self.ST = np.concatenate(
                (prev_nodes * self.u, [prev_nodes[-1] * self.m, prev_nodes[-1] * self.d]))
            self.STs.append(self.ST)
            
    def traverse_tree(self, payoffs):
        ''' Traverse the tree backwards '''
        for i in reversed(range(self.N)):
            payoffs = (payoffs[:-2] * self.qu + payoffs[1:-1] * self.qm + payoffs[2:] *self.qd) * self.df
            
            if not self.is_european:
                payoffs = self.check_early_exercise(payoffs, i)
        
        return payoffs

def main():

    eu_put = TrinomialOption(50, 50, 0.05, 0.5, 2, {'sigma':0.3, 'is_call':False})
    print("European put: %s" % eu_put.price())

    am_put = TrinomialOption(50, 50, 0.05, 0.5, 2, {'sigma':0.3, 'is_call':False, 'is_eu': False})
    print("European put: %s" % am_put.price())

 
if __name__ == '__main__':
    main()