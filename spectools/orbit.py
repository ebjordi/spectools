import numpy as np
import pandas as pd

def phase( JD, T0 = 57880.63, P = 29.1333, mean_anomaly = False):
    """Returns phase given orbital parameters, default parameteres are for i 
    Orionis params updated to Eguren 2021"""
    JD = JD * np.ones_like(JD)
    T0 = T0 * np.ones_like(JD)
    pha = (JD - T0) / P
    pha = pha - pha.astype(int)
    if isinstance(pha,np.float64):
        if pha < 0: pha += 1
    else:
        pha[pha<0.] += 1. 
    if mean_anomaly:
        return 2*np.pi*pha
    return pha

def excentric_anomaly(phi, e = 0.734, mean_anomaly = False):
    """Returns excentric anomaly given a mean anomaly(phase) and other orbital parameters
    Default values are for i Ori ofund in Eguren 2018"""
    phi = phi * np.ones_like(phi)
    E0 = phi * np.ones_like(phi)
    if not mean_anomaly:
        E0 =  E0 * 2 * np.pi
        phi =  phi * 2 * np.pi
    count = 0
    no_convergence = True
    while no_convergence:
        count += 1
        E = E0 - (( E0 - e * np.sin(E0) - phi)/ (1 - e * np.cos(E0)))
        if isinstance(E, np.float64):
            if np.isclose(E, E0): return E
        elif np.allclose(E, E0):  return E
        E0 = E
        if count > 10000:
            print(count)
            raise ValueError("Too many iteration")

def true_anomaly(excentric_anomaly, e = 0.734):
    """Returns true anomaly give an excentric anomaly and excentricity"""

    E = excentric_anomaly * np.ones_like(excentric_anomaly)
    theta = 2 * np.arctan(np.sqrt((1 + e)/(1 - e)) * np.tan(E/2))

    if isinstance(theta,np.ndarray):
        theta[theta < 0] = theta[theta < 0] + 2 * np.pi
    elif theta < 0:
        theta += 2 * np.pi

    return theta

def rv(true_anomaly, K = 108.3, e=0.734,omega = 126.3,gamma = 34):
    ω = omega * np.pi / 180
    θ = true_anomaly
    Vrad = K * (np.cos(θ + ω) + e * np.cos(ω))
    return Vrad + gamma

def velocity_curve_jd(JD, T0 = 57880.63, P = 29.1333, e = 0.734, K = 108.3, omega = 126.3, gamma = 34):
    φ = phase(JD, T0 =T0 ,P = P)
    E = excentric_anomaly(φ, e=e)
    θ = true_anomaly(E, e = e)
    vr = rv(θ, K = K, omega = omega, gamma = gamma)
    return vr

def velocity_curve_from_phase(points = 100, a = 0, b = 1.2, e = 0.734, K = 108.3, omega = 126.3, gamma = 34):
    φ = np.linspace(a, b, points)
    E = excentric_anomaly(φ, e = e)
    θ = true_anomaly(E, e = e)
    vr = rv(θ, K = K, omega = omega, gamma = gamma)
    return vr

def orbit_function(kepler_file : str):
    """Given a kepler output file returns interpolated funtions for primary and
    secondary components of a binary system"""
    names = ['fase','vr-p','vr-s']
    df = pd.read_table(kepler_file,names=names,sep='\s+', skiprows=1 ,index_col=False)
    primary =   interp1d(df["fase"],df["vr-p"], kind='cubic')
    secondary = interp1d(df["fase"],df["vr-s"], kind='cubic')
    return primary, secondary
