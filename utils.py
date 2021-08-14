import astropy.io.fits as pf


def get_keyword(header,keyword : str):
    """Extracts keyword from header spectra"""
    return header.get(keyword)


def wavelength(header):
    wave = [header['CRVAL1'] + header['CDELT1'] * i for i in range(header['NAXIS1'])]
    return wave
