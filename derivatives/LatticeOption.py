#!/usr/bin/env python
# coding: utf-8


import numpy as np
from BinomialTreeOption import BinomialOption
from TrinomialTreeOption import TrinomialOption


class BinomialLattice(BinomialOption):

    def setup_parameters(self):
        '''Required calculations for the model '''
        super(BinomialLattice, self).setup_parameters()
        self.M = 2 * self.N + 1

    def initialize_stock_price_tree(self):
        self.STs = np.zeros(self.M)
        self.STs[0] = self.S0 * self.u ** self.N
        
        for i in range(1, self.M):
            self.STs[i] = self.STs[i - 1] * self.d
            
    def initialize_payoffs_tree(self):
        odd_nodes = self.STs[::2]
        return np.maximum(0, (odd_nodes - self.K) if self.is_call else (self.K - odd_nodes))
    
    def check_early_exercise(self, payoffs, node):
        self.STs = self.STs[1:-1] # Shorten the ends of the list
        odd_STs = self.STs[::2]
        early_ex_payoffs = (odd_STs - self.K) if self.is_call else (self.K - odd_STs)
        payoffs = np.maximum(payoffs, early_ex_payoffs)
        
        return payoffs


class TrinomialLattice(TrinomialOption):
    
    def setup_parameters(self):
        super(TrinomialLattice, self).setup_parameters()
        self.M = 2 * self.N + 1
    
    def initialize_stock_price_tree(self):
        self.STs = np.zeros(self.M)
        self.STs[0] = self.S0 * self.u ** self.N
        
        for i in range(1, self.M):
            self.STs[i] = self.STs[i-1] * self.d
    
    def initialize_payoffs_tree(self):
        return np.maximum(0, (self.STs - K) if self.is_call else (self.K - self.STs))
    
    def check_early_exercise(self, payoffs, node):
        self.STs = self.STs[1:-1] # Shorten the ends of list
        early_ex_payoff = (self.STs - self.K) if self.is_call else (self.K - self.STs)
        payoffs = np.maximum(payoffs, early_ex_payoff)
        
        return payoffs



def main():

    print("Using Binomial Lattice: ")
    eu_put = BinomialLattice(50, 50, 0.05, 0.5, 2, {'pu':0.2, 'pd':0.2, 'is_call':False, 'is_eu':False})
    print("European put: %s" % eu_put.price())

    print('------******------')
    am_put = BinomialLattice(50, 50, 0.05, 0.5, 2, {'pu':0.2, 'pd':0.2, 'is_call':False})
    print("European put: %s" % am_put.price())


    print('\n')
    print("Using Trinomial Lattice: ")
    eu_put = TrinomialLattice(50, 50, 0.05, 0.5, 2, {'sigma':0.3, 'is_call':False, 'is_eu': False})
    print("European put: %s" % eu_put.price())

    print('------******------')
    am_put = TrinomialLattice(50, 50, 0.05, 0.5, 2, {'sigma':0.3, 'is_call':False, 'is_eu': False})
    print("European put: %s" % am_put.price())


if __name__ == '__main__':
    main()