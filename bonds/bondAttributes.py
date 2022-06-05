#!/usr/bin/env python
# coding: utf-8

import numpy as np
import scipy.optimize as opt


def bond_ytm(price, par, T, coup, freq=2, guess=0.5):
    """ Get the yield-to-maturity of a bond """
    freq = float(freq)
    periods = freq * T
    coupon = coup / 100 * par / freq
    dt = [(i + 1) / freq for i in range(int(periods))]

    def ytm_func(y): return np.sum([coupon / (1 + y / freq) ** (freq * t)
                                    for t in dt]) + par / (1+y / freq) ** (freq * T) - price

    return opt.newton(ytm_func, guess)


def bond_price(par, T, ytm, coup, freq=2):
    """ Get bond price from YTM """
    freq = float(freq)
    periods = T * freq
    coupon = coup / 100 * par / freq
    dt = [(i + 1) / freq for i in range(int(periods))]
    price = np.sum([coupon / (1 + ytm / freq) ** (freq * t)
                    for t in dt]) + par / (1+ytm / freq) ** (freq * T)
    return price


def bond_mod_duration(price, par, T, coup, freq, dy=0.01):
    """ Calcualte modified duration of a bond """
    ytm = bond_ytm(price, par, T, coup, freq)

    ytm_minus = ytm - dy
    price_minus = bond_price(par, T, ytm_minus, coup, freq)

    ytm_plus = ytm + dy
    price_plus = bond_price(par, T, ytm_plus, coup, freq)

    duration = (price_minus - price_plus) / (2 * price * dy)
    return duration


def bond_convexity(price, par, T, coup, freq, dy=0.01):
    """ Calcualte convexity of a bond """
    ytm = bond_ytm(price, par, T, coup, freq)

    ytm_minus = ytm - dy
    price_minus = bond_price(par, T, ytm_minus, coup, freq)

    ytm_plus = ytm + dy
    price_plus = bond_price(par, T, ytm_plus, coup, freq)

    convexity = (price_minus + price_plus - 2 * price) / (price * dy ** 2)
    return convexity 

