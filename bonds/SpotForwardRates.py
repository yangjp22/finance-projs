#!/usr/bin/env python
# coding: utf-8

import numpy as np


class BootStrapYieldCurve(object):

    def __init__(self):
        self.zero_rates = dict()   # Map each T to a zero rate
        self.instruments = dict()   # Map each T to an instrument

    def add_instrument(self, par, T, coup, price, compounding_freq=2):
        """ Save instrument information by maturity """
        self.instruments[T] = (par, coup, price, compounding_freq)

    def get_zero_rates(self):
        """ Calculate a list of available zero rates """
        self.bootstrap_zero_coupons()
        self.get_bond_spot_rates()
        return [self.zero_rates[T] for T in self.get_maturities()]

    def get_maturities(self):
        """ Return sorted maturities from added instruments. """
        return sorted(self.instruments.keys())

    def bootstrap_zero_coupons(self):
        """ Get zero rates from zero coupon bonds """
        for T in self.instruments:
            (par, coup, price, freq) = self.instruments[T]
            if coup == 0:
                self.zero_rates[T] = self.zero_coupon_spot_rate(par, price, T)

    def get_bond_spot_rates(self):
        """ Get spot rates for every maturity available """
        for T in self.get_maturities():
            instrument = self.instruments[T]
            (par, coup, price, freq) = instrument

            if coup != 0:
                self.zero_rates[T] = self.calculate_bonc_spot_rate(
                    T, instrument)

    def calculate_bonc_spot_rate(self, T, instrument):
        """ Get spot rate of a bond by bootstrapping """
        try:
            (par, coup, price, freq) = instrument
            periods = T * freq   # Number of coupon payments
            value = price
            per_coupon = coup / freq  # coupon per period

            for i in range(int(periods) - 1):
                t = (i + 1) / float(freq)
                spot_rate = self.zero_rates[t]
                discounted_coupon = per_coupon * np.exp(-spot_rate * t)
                value -= discounted_coupon

            # Derive spot rate for a particular maturity
            last_period = int(periods) / float(freq)
            spot_rate = -np.log(value / (par + per_coupon)) / last_period
            return spot_rate

        except:
            print("Error: spot rate not found for T=%s" % t)

    def zero_coupon_spot_rate(self, par, price, T):
        """ Get zero rate of a zero coupon bond """
        spot_rate = np.log(par / price) / T
        return spot_rate


class ForwordRates(object):

    def __init__(self):
        self.forward_rates = []
        self.spot_rates = dict()

    def add_spot_rate(self, T, spot_rate):
        self.spot_rates[T] = spot_rate

    def calculate_forward_rate(self, T1, T2):
        R1 = self.spot_rates[T1]
        R2 = self.spot_rates[T2]
        forward_rate = (R2 * T2 - R1*T1) / (T2 - T1)
        return forward_rate

    def get_forward_rates(self):
        periods = sorted(self.spot_rates.keys())
        for T2, T1 in zip(periods, periods[1:]):
            forward_rate = self.calculate_forward_rate(T2, T1)
            self.forward_rates.append(forward_rate)
        return self.forward_rates

