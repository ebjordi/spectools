import astropy.io.fits as pf
from numpy import array as nparray
from datetime import datetime

def get_keyword(header,keyword : str):
    """Extracts keyword from header spectra"""
    return header.get(keyword)


def wavelength(header):
    wave = [header['CRVAL1'] + header['CDELT1'] * i for i in range(header['NAXIS1'])]
    return nparray(wave)


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
