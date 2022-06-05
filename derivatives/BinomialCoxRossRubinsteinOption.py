#!/usr/bin/env python
# coding: utf-8

import numpy as np
from BinomialTreeOption import BinomialOption


class BinomialCRROption(BinomialOption):

    def setup_parameters(self):
        self.u = np.exp(self.sigma * np.sqrt(self.dt))
        self.d = 1 / self.u
        self.qu = (np.exp((self.r - self.div) * self.dt) -
                   self.d) / (self.u - self.d)
        self.qd = 1 - self.qu

def main():

    eu_option = BinomialCRROption(50, 50, 0.05, 0.5, 2, {'sigma':0.3, 'is_call':False})
    print("European Option: %s" % eu_option.price())

    am_option = BinomialCRROption(50, 50, 0.05, 0.5, 2, {'sigma':0.3, 'is_call':False, 'is_eu':False})
    print("American Option: %s" % am_option.price())


if __name__ == '__main__':
    main()