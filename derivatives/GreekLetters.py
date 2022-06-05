#!/usr/bin/env python
# coding: utf-8

import numpy as np
from BinomialLeisenReimerOption import BinomialLROption


class BinomialLRWithGreeks(BinomialLROption):

    def new_stock_price_tree(self):
        ''' Create additional layer of nodes to our original stock price tree '''
        self.STs = [
            np.array([self.S0 * self.u / self.d, self.S0, self.S0 * self.d / self.u])]

        for i in range(self.N):
            prev_branches = self.STs[-1]
            st = np.concatenate(
                (prev_branches * self.u, [prev_branches[-1] * self.d]))
            self.STs.append(st)

    def price(self):
        self.setup_parameters()
        self.new_stock_price_tree()
        payoffs = self.begin_tree_traversal()

        ''' Option value is now in the middle node at t=0'''
        option_value = payoffs[int(len(payoffs) / 2)]
        payoff_up = payoffs[0]
        payoff_down = payoffs[-1]
        S_up = self.STs[0][0]
        S_down = self.STs[0][-1]
        dS_up = S_up - self.S0
        dS_down = self.S0 - S_down

        ''' Get delat value '''
        dS = S_up - S_down
        dV = payoff_up - payoff_down
        delta = dV / dS

        ''' Get gamma vlaue '''
        gamma = ((payoff_up - option_value) / dS_up - (option_value - payoff_down) /
                 dS_down) / ((self.S0 + S_up) / 2 - (self.S0 + S_down) / 2)
    
        return option_value, delta, gamma


def main():

    en_call = BinomialLRWithGreeks(50, 50, 0.05, 0.5, 300, {'sigma':0.3, 'is_call':True})
    results = en_call.price()
    print("European call values")
    print("Price: %s\nDelta: %s\nGamma: %s" % results)

    print("-----*****-----")

    en_put = BinomialLRWithGreeks(50, 50, 0.05, 0.5, 300, {'sigma':0.3, 'is_call':False})
    results = en_put.price()
    print("European put values")
    print("Price: %s\nDelta: %s\nGamma: %s" % results)


if __name__ == '__main__':
    main()