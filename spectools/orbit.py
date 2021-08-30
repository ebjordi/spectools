import numpy as np
import pandas as pd

def phase( JD, T0 = 2455608.29, P = 29.1350, mean_anomaly = False):
    """Returns phase given orbital parameters, default parameteres are for i 
    Orionis params updated to Eguren 2021""" 
    if isinstance(JD, (np.ndarray,list)): 
        T0 = T0 * np.ones_like(JD)
        JD = np.array(JD)
        pha = (JD - T0) / P
        pha = pha - pha.astype(int)
    elif isinstance(JD,float):
        pha = (JD - T0) / P
        pha = pha - int(pha)
    if mean_anomaly:
        return 2*np.pi*pha
    return pha

def excentric_anomaly(phi, T0 = 2455608.29, P = 29.1350, e = 0.732,
                      mean_anomaly = False):
    """Returns excentric anomaly given a mean anomaly(phase) and other orbital parameters
    Default values are for i Ori ofund in Eguren 2018"""
    E0 = phi * np.ones_like(phi)
    if not mean_anomaly:
        E0 =  E0 * 2 * np.pi
    contador = 0
    no_convergence = True
    while no_convergence:
        contador += 1
        E = E0 - (( E0 - e * np.sin(E0) - phi)/ (1 - e * np.cos(E0)))
        if abs(E - E0).all() < 1e-6:
            return E
        else:
            E0 = E
        if contador > 10000:
            raise("Too many iteration")

def true_anomaly(excentric_anomaly, e = 0.732):
    """Returns true anomaly give an excentric anomaly and excentricity"""


    theta = 2 * np.arctan(np.sqrt((1 + e)/(1 - e)) * np.tan(E/2))

    if isinstance(theta,np.ndarray):
        theta[theta < 0] = theta[theta < 0] + 2 * np.pi
    else:
        if theta < 0:
            theta += 2 * np.pi
    return theta


def orbit_function(kepler_file : str):
    """Given a kepler output file returns interpolated funtions for primary and
    secondary components of a binary system"""
    names = ['fase','vr-p','vr-s']
    df = pd.read_table(kepler_file,names=names,sep='\s+', skiprows=1 ,index_col=False)
    primary =   interp1d(df["fase"],df["vr-p"], kind='cubic')
    secondary = interp1d(df["fase"],df["vr-s"], kind='cubic')
    return primary, secondary
