import numpy as np


def gaussian(x,cont,inten,m,sigma):
    """Return gaussian model of length x"""
    return cont - inten*np.exp(-((x-m)/sigma)**2)


def gaussians(x,cont,inten1,m1,sigma1,inten2,m2,sigma2):
    """Return gaussian model of length x"""
    return cont - inten1*np.exp(-((x-m1)/sigma1)**2) - inten2*np.exp(-((x-m2)/sigma2)**2)
