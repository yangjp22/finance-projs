#!/usr/bin/env python
# coding: utf-8

import numpy as np
from StockOption import StockOption


class BinomialOption(StockOption):

    """ Required calculation for the model """
    """ Setup the parameters """

    def setup_parameters(self):
        self.u = self.pu + 1  # Expected value in the up state
        self.d = 1 - self.pd   # Expected value in the down state
        self.qu = (np.exp((self.r - self.div) * self.dt) -
                   self.d) / (self.u - self.d)
        self.qd = 1 - self.qu

    def initialize_stock_price_tree(self):
        # Initialize a 2D tree at T = 0
        self.STs = [np.array([self.S0])]

        # Stimulate the possible stock prices path
        for i in range(self.N):
            prev_branches = self.STs[-1]
            st = np.concatenate(
                (prev_branches * self.u, [prev_branches[-1] * self.d]))
            self.STs.append(st)  # Add nodes at each time step

    def initialize_payoffs_tree(self):
        # Get payoffs when the option expires at terminal nodes
        payoffs = np.maximum(0, (self.STs[-1] - self.K)
                             if self.is_call else (self.K - self.STs[-1]))
        
        return payoffs

    def check_early_exercise(self, payoffs, node):
        early_ex_payoff = (
            self.STs[node] - self.K) if self.is_call else (self.K - self.STs[node])
        return np.maximum(payoffs, early_ex_payoff)
    
    def traverse_tree(self, payoffs):
        # Starting from the time the option expires, traverse
        # backwards and calculate discouned payoffs at each node
        for i in reversed(range(self.N)):
            payoffs = (payoffs[: -1] * self.qu + payoffs[1:] * self.qd) * self.df
            
            # Payoffs from exercising, for American options
            if not self.is_european:
                payoffs = self.check_early_exercise(payoffs, i)

        return payoffs

    def begin_tree_traversal(self):
        payoffs = self.initialize_payoffs_tree()
        return self.traverse_tree(payoffs)

    def price(self):
        """ The pricing implementation"""
        self.setup_parameters()
        self.initialize_stock_price_tree()
        payoffs = self.begin_tree_traversal()
        return payoffs[0]  # Option value converges to first node


def main():

    eu_option = BinomialOption(50, 50, 0.05, 0.5, 2, {'pu':0.2, 'pd':0.2, 'is_call':False})
    print("European Option: %s" % eu_option.price())

    am_option = BinomialOption(50, 50, 0.05, 0.5, 2, {'pu':0.2, 'pd':0.2, 'is_call':False, 'is_eu':False})
    print("American Option: %s" % am_option.price())


if __name__ == '__main__':
    main()