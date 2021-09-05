import astropy.io.fits as pf
from scipy.interpolate import interp1d
import pandas as pd
from specutils import Spectrum1D
from spectools.utils import wavelength

def open(filename, normalized = True):
    """Extract wavelengh and flux for FIES and HERMES spectra"""
    hdu = pf.open(filename)
    data = hdu[0].data
    header = hdu[0].header
    if normalized:
        wave = wavelength(header)
        return Spectrum1D(flux=data[0],spectral_axis=wave),header
    return Spectrum1D(flux=data[1],spectral_axis=data[0]),header

