import astropy.io.fits as pf
from specutils.spectra import Spectrum1D, SpectralRegion
from specutils.fitting import fit_generic_continuum
from astropy.modeling.models import Chebyshev1D
from specutils.manipulation import LinearInterpolatedResampler
from pyspeckit import Spectrum

def extract_line(file,center,order,regions,**kwargs):
    """Extract line from SONG spectrum and fit fit_continuum. 
    For usage on other lines, `exclude_regions` in `fit` """
    data = pf.getdata(file) # Get the data
    header = pf.getheader(file) # Get the full header
    x = data[3,order,:]
    y = data[0,order,:]
    blaze=data[2,order,:]
    line = Spectrum1D(flux=(y/blaze)*u.adu, spectral_axis=x*u.Angstrom, **kwargs)
    fit = fit_generic_continuum(line,model=Chebyshev1D(4),exclude_regions=regions)
    line = (line / fit(x*u.Angstrom))
    return line, header

def resample(spectrum):
    """Return a resampled spectrum with equidistant spectral axis"""
    resampler = LinearInterpolatedResampler(extrapolation_treatment='zero_fill')
    x = np.linspace(spectrum.spectral_axis[0].value,spectrum.spectral_axis[-1].value,2048)
    return resampler.resample1d(spectrum,x*u.Angstrom)

def save(spectrum,name, header = None):
    """The only method I know so far to save a custom spectrum. Requires
    equidistant spectral_axis"""
    if header is None:
        header = spectrum.header
    new_spectrum = Spectrum(xarr=spectrum.spectral_axis, data = spectrum.flux,
                           header=header)
    new_spectrum.write(name + '.fits', type='fits')


