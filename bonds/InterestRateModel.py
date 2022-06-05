#!/usr/bin/env python
# coding: utf-8

import numpy as np


def Vasicek(r0, K, theta, sigma, T=1, N=10, seed=777):
    """ Simulate interest rate path by the Vasicek model """
    """ The interest may be negative"""
    """ Mean-revertion """
    np.random.seed(seed)
    dt = T / N
    rates = [r0]
    for i in range(N):
        dr = K * (theta - rates[-1]) * dt + sigma * np.random.normal()
        rates.append(rates[-1] + dr)

    return range(N + 1), rates


def CIR(r0, K, theta, sigma, T=1, N=10, seed=777):
    """ Simulate interest rate path by the CIR model """
    """ Won't be negative """
    """ Mean-revertion """
    np.random.seed(seed)
    dt = T / N
    rates = [r0]
    for i in range(N):
        dr = K * (theta - rates[-1]) * dt + sigma * np.sqrt(rates[-1]) * np.random.normal()
        rates.append(rates[-1] + dr)

    return range(N + 1), rates


def rendleman_bartter(r0, theta, sigma, T=1, N=10, seed=777):
    """ Simulate interest rate path by the Rendleman-Barter model """
    """ No mean-revertion """
    """ Geometric Brownian Motion"""
    np.random.seed(seed)
    dt = T / N
    rates = [r0]
    for i in range(N):
        dr = theta * rates[-1] * dt + sigma * rates[-1] * np.random.normal()
        rates.append(rates[-1] + dr)

    return range(N + 1), rates


def brennan_schwartz(r0, K, theta, sigma, T=1, N=10, seed=777):
    """ Simulate interest rate path by the Brennan Schwartz model """
    """ Mean-revertion """
    """ Geometric Brownian Motion """
    np.random.seed(seed)
    dt = T / N
    rates = [r0]
    for i in range(N):
        dr = K * (theta - rates[-1]) * dt + sigma * rates[-1] * np.random.normal()
        rates.append(rates[-1] + dr)

    return range(N + 1), rates

