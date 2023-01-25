import astropy.io.fits as pf
import astropy.constants as c
import numpy as np
from datetime import datetime
from scipy.interpolate import interp1d
from typing import Union

def get_keyword(header,keyword : str):
    """Extracts keyword from header spectra"""
    return header.get(keyword)


def wavelength(header):
    wave = [header['CRVAL1'] + header['CDELT1'] * i for i in range(header['NAXIS1'])]
    return np.array(wave)


def add_UT_to_header(spectra):
    for spectrum in spectra:
        spec = pf.open(spectrum, verify = False)
        data = spec[0].data
        header = spec[0].header
        date_key = 'DATE_OBS'
        date,ut =header[date_key].split('T')
        ut = datetime.strptime(ut,'%H:%M:%S.%f')
        ut_float = ut.hour +ut.minute / 60. +ut.second / 3600.
        header["EPOCH"]= 2000.0
        header["UT"]=ut_float
        pf.writeto(spectrum,data,header,output_verify='ignore',overwrite=True)


def mask_line(x,y,a,b):
    """returns masked arrays of x[a < x < b] y[a < x < b]
    """
    x_ma=np.ma.masked_outside(x,a,b)
    mask = np.ma.getmask(x_ma)
    f_ma=np.ma.array(y,mask=mask)    
    return x_ma,f_ma

def open_file(filename): #for 1Dspecs ?
    hdu = pf.open(filename)
    data = hdu[0].data
    header = hdu[0].header
    wave = wavelength(header)
    return wave,data

def ascii_spec(filename):
    a = np.genfromtxt(filename,delimiter = '  ')
    w = a[:,0]
    f = a[:,-1]
    return w,f


def shift(wvl,flux,v,new_wvl = None):
    cvel =  c.c.to('km/s').value
    wlprime = wvl * (1.0 + v / cvel)
    if new_wvl is not None:
        wvl = new_wvl
    nflux = interp1d(wlprime, flux, bounds_error=False, fill_value=1)(wvl)
    return nflux    

def cut_resample(w_model,f_model,w_obj,f_obj,a,b):
    x_o = np.where((w_obj>a)&(w_obj<b),w_obj,0)
    y_o = f_obj[x_o>0]
    x_o = x_o[x_o>0]
    
    x_e = np.where((w_model>a)&(w_model<b),w_model,0)
    y_e = f_model[x_e>0]
    x_e = x_e[x_e>0]
    y_e = interp1d(x_e, y_e, bounds_error=False, fill_value=1)(x_o)
    return x_o,y_o,y_e


def get_keyword(file : str,keyword : str):
    """Extracts keyword from header spectra"""
    header = pf.getheader(file)
    return header.get(keyword)


#set the templates to 0 km/s
def displacement_avg(measurements : Union(list, np.array), star):
    """Calculate redshift velocities and average velocity starting for lines meassured by hand
    Tailored for Iota Ori A"""
    lambda_0 = np.array([4025.6, 4713.146, 4921.931, 5015.68, 5411.52, 5592.252])
    cvel =  c.c.to('km/s').value

    if star == 'secondary':
        lambda_0 = lambda_0[:-2]
    vels = cvel * (np.array((measurements) - lambda_0) / lambda_0)
    return vels,vels.mean()

def displacement(measurement, line, star):
    """Calculate redshift velocity for lines meassured 
    Tailored for Iota Ori A"""
    cvel =  c.c.to('km/s').value

    if isinstance(line, int):
        lambda_0 = lines_dict[str(line)]
    else:
        lambda_0 = line

    lines_dict = {4025:4025.6, 4713 : 4713.146, 4921 : 4921.931, 5015 : 5015.68, 5411 : 5411.52, 5592 : 5592.252}

    if star == 'secondary':
        lambda_0 = lambda_0[:-2]
    vels = cvel * (np.array((measurement) - lambda_0) / lambda_0)
    avg = vels.mean()


def open_shift(A : str, B : str , va : Union(float, np.float64), vb : Union(float, np.float64), 
               a : Union(float,np.float64) = None, b : Union(float,np.float64) = None ):
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


def cut_resample(w_model,f_model,w_obj,f_obj,a,b):
    x_o = np.where((w_obj>a)&(w_obj<b),w_obj,0)
    y_o = f_obj[x_o>0]
    x_o = x_o[x_o>0]
    
    x_e = np.where((w_model>a)&(w_model<b),w_model,0)
    y_e = f_model[x_e>0]
    x_e = x_e[x_e>0]
    y_e = interp1d(x_e, y_e, bounds_error=False, fill_value=1)(x_o)
    return x_o,y_o,y_e