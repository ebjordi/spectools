import astropy.io.fits as pf
from scipy.interpolate import interp1d
import pandas as pd

def extract_spectrum(filename, normalized = True):
    """Extract wavelengh and flux for FIES and HERMES spectra"""
    hdu = pf.open(filename)
    data = hdu[0].data
    header = hdu[0].header
    wave = wavelength(header)
    if normalized:
        return wave,data[0],header
    return Spectrum1d(flux=data[1],spectral_axis=data[0]),header

def orbit_function(kepler_file : str):
    """Given a kepler output file returns interpolated funtions for primary and
    secondary components of a binary system"""
    names = ['fase','vr-p','vr-s']
    df = pd.read_table(kepler_file,names=names,sep='\s+', skiprows=1 ,index_col=False)
    
    primary =   interp1d(df["fase"],df["vr-p"], kind='cubic')
    secondary = interp1d(df["fase"],df["vr-s"], kind='cubic')
    return primary, secondary

