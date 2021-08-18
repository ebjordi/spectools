import numpy as np


def phi( HDJ, T0 = 245780.91, P = 29.1325, mean_anomaly = False):
    """Returns phase given orbital parameters, default parameteres are for i Orionis params
    found in Eguren 2018"""

    phase = (HDJ - T0) / P
    if mean_anomaly:
        phase = 2 * np.pi * phase
    return fases - int(fases) 

def excentric_anomaly(phi, T0 = 2455608.11, P = 29.1350, e = 0.713):
    """Returns excentric anomaly given a mean anomaly(phase) and other orbital parameters
    Default values are for i Ori ofund in Eguren 2018"""
    phi = 2 * np.pi * phi
    contador = 0
    no_convergence = True
    E_0 = phi
    while no_convergence:
        contador = contador + 1
        E = E_0 - (( E_0 - e * np.sin(E_0) - phi)/ (1 - e * np.cos(E_0)))
        if isinstance(E,np.ndarray):
            if abs(E - E_0).all() < 1e-6:
                return E
            else:
                E_0 = E
            if contador > 10000:
                raise("Too many iteration")
        else:
            if abs(E - E_0) < 1e-6:
                return E
            else:
                E_0 = E

def true_anomaly(excentric_anomaly, e = 0.732):
    """Returns true anomaly give an excentric anomaly and excentricity"""


    theta = 2 * np.arctan(np.sqrt((1 + e)/(1 - e)) * np.tan(E/2))

    if isinstance(theta,np.ndarray):
        theta[theta < 0] = theta[theta < 0] + 2 * np.pi
    else:
        if theta < 0:
            theta = theta + 2 * np.pi
    return theta
