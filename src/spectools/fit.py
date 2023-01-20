from itertools import product
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from spectools.utils import cut_resample
from typing import Union
from astropy.constants import c
import astropy.io.fits as pf
from orbit import Orbit

def main():
    wo,fo=open_file('HD37043_20170408_201940_M_V85000.fits')
    fo = fo[0]

    A = 'T350g370.asc'
    B = 'T300g380.asc'
    v1=-100
    v2=300

    w1, fa_s, fb_s = open_shift(A,B,v1,v2,b=7000)

    dils = [0.6,0.65,0.7,0.75,0.8,0.85]
    lines=[(4080,4112),(4330,4346),(4845,4875),(4019,4035),(5868,5885),(4682,4693),(4197,4203),(4537,4543),(4682,4686),(5400,5417)]
    #Esto son etiquetas para el mapa de color

    labels_y = [str(d) for d in dils]
    labels_x = [str(l) for l in lines]

    tests = OC_dils(w1,fa_s,fb_s,wo,fo,dils,lines)
    print(tests)
    return


def OC_dils(w_model :  Union(np.array), f_model_a :  Union(np.array), f_model_b :  Union(np.array),
            w_object :  Union(np.array), f_object :  Union(np.array), dilutions :  Union(list,np.array), regions :  Union(list,np.array)):

    #Hacemos una matriz de (O-C)**2 donde las filas son dilusion y las columnas regiones que pasamos como argumento
    region_oc = np.ndarray((len(dilutions),len(regions)))
    for i,d in enumerate(dilutions):
        fa_ = f_model_a * d
        fb_ = f_model_b * (1-d)
        f1 = fa_+fb_
        for j,ab in enumerate(regions):
            a,b=ab
            x,y,y_model = cut_resample(w_model,f1,w_object,f_object,a,b)
            region_oc[i][j] = (np.square(y-y_model) / y_model).sum()
    return region_oc

def open_shift(A : str, B : str , va :  Union(float, np.float64), vb :  Union(float, np.float64), 
               a :  Union(float,np.float64) = None, b :  Union(float,np.float64) = None ):
    wa,fa = ascii_spec(A)
    wb,fb = ascii_spec(B)
    #Aplico cotas 
    if a is not None:
        fa = fa[wa>a]
        wa = wa[wa>a]
        fb = fb[wb>a]
        wb = wb[wb>a]
    if b is not None:
        fa = fa[wa<b]
        wa = wa[wa<b]
        fb = fb[wb<b]
        wb = wb[wb<b]
    fa_shift = shift(wa, fa, va)
    fb_shift = shift(wb, fb, vb, wa)#va a resamplear con el eje de wa, 
                                    #si son modelos del mismo programa 
                                    #deberían ser similares, pero el 
                                    #doppler shift puede cambiarlo
    #Me aseguro que los arrays tengan el mismo largo
    if len(fb_shift) > len(fa_shift):
        arr_len = len(fa_shift)
    else: arr_len = len(fb_shift)
    
    w1=wa[:arr_len]
    fa_s=fa_shift[:arr_len]
    fb_s=fb_shift[:arr_len]
    # A partir de acá los dos modelos tienen el mismo eje de dispersion
    return w1,fa_s,fb_s


def ascii_spec(filename):
    a = np.genfromtxt(filename,delimiter = '  ')
    w = a[:,0]
    f = a[:,-1]
    return w,f

def shift(wvl,flux,v,new_wvl = None):
    cvel = c.to('km/s').value
    wlprime = wvl * (1.0 + v / cvel)
    if new_wvl is not None:
        wvl = new_wvl
    nflux = interp1d(wlprime, flux, bounds_error=False, fill_value=1)(wvl)
    return nflux

def open_file(filename): #for 1Dspecs ?
    hdu = pf.open(filename)
    data = hdu[0].data
    header = hdu[0].header
    wave = wavelength(header)
    return wave,data


def wavelength(header):
    wave = [header['CRVAL1'] + header['CDELT1'] * i for i in range(header['NAXIS1'])]
    return np.array(wave)


if __name__ == '__main__':
    main()
