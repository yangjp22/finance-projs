#!/usr/bin/env python
# coding: utf-8

import numpy as np
from matplotlib import pyplot as plt

def exact_zcb(theta, kappa, sigma, tau, r0=0.):
    """ Get zero coupon bond price by Vasicek model """
    B = (1 - np.exp(-kappa * tau)) / kappa
    A = np.exp((theta - (sigma ** 2) / (2 * (kappa ** 2))) *
               (B - tau) - (sigma ** 2) / (4 * kappa) * (B ** 2))
    return A * np.exp(-r0 * B)

def exercise_early(K, R, t):
    return K * np.exp(-R * t)

def callable(theta, kappa, sigma, tau, k, r0=0.):
    zcb = exact_zcb(theta, kappa, sigma, tau, r0)
    early = exercise_early(k, r0, tau)
    return np.minimum(zcb, early)


def main():

    Ts = np.r_[0.0 : 25.5 : 0.5]
    zcbs = [exact_zcb(0.5, 0.02, 0.03, t, 0.015) for t in Ts]

    plt.subplots(3, 1)
    plt.subplot(3, 1, 1)
    plt.title("Zero Coupon Bond (ZCB) Values by Time")
    plt.plot(Ts, zcbs, label='ZCB')
    plt.ylabel('Value ($)')
    plt.legend()
    plt.grid(True)


    zcbs = [exact_zcb(0.5, 0.02, 0.03, t, 0.015) for t in Ts]
    Ks = [exercise_early(0.95, 0.015, t) for t in Ts]
    plt.subplot(3, 1, 2)
    plt.title("Zero Coupon Bond (ZCB) Values and Strike (K) Values by Time")
    plt.plot(Ts, zcbs, label='ZCB')
    plt.plot(Ts, Ks, label = 'Ks', linestyle='--',marker='.')
    plt.ylabel('Value ($)')
    plt.xlabel('Time in years')
    plt.legend()
    plt.grid(True)


    call = [callable(0.5, 0.02, 0.03, t, 0.95, 0.015) for t in Ts]
    plt.subplot(3, 1, 3)
    plt.title("Callable bond Values by Time")
    plt.plot(Ts, call, label='Callable', linestyle='--', marker='.')
    plt.ylabel('Value ($)')
    plt.xlabel('Time in years')
    plt.legend()
    plt.grid(True)

    plt.show()


if __name__ == '__main__':
    main()