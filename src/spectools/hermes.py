import astropy.io.fits as pf
from astropy import units as u
from specutils import Spectrum1D
from spectools.utils import wavelength

def open(filename, normalized = True):
    """Extract wavelengh and flux for FIES and HERMES spectra"""
    hdu = pf.open(filename)
    data = hdu[0].data
    header = hdu[0].header
    if normalized:
        wave = wavelength(header)
        return Spectrum1D(flux=data*u.adu,spectral_axis=wave*u.Angstrom),header
    return Spectrum1D(flux=data[1]*u.adu,spectral_axis=data[0]*u.Angstrom),header

