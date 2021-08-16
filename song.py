import astropy.io.fits as pf
from specutils.spectra import Spectrum1D, SpectralRegion
from specutils.fitting import fit_continuum,fit_generic_continuum
from astropy.modeling.models import Polynomial1D,Const1D,Chebyshev1D
from specutils.manipulation import LinearInterpolatedResampler
from pyspeckit import Spectrum

def extract_line(file,center,order,**kwargs):
    lines={5015: 17,
           5811: 34}
    data = pf.getdata(file) # Get the data
    header = pf.getheader(file) # Get the full header
    x = data[3,order,:]
    y = data[0,order,:]
    blaze=data[2,order,:]
    line = Spectrum1D(flux=(y/blaze)*u.adu, spectral_axis=x*u.Angstrom, **kwargs)
    g1_fit = fit_generic_continuum(line,model=Chebyshev1D(4),exclude_regions=[
                                    SpectralRegion(line.spectral_axis[0],line.spectral_axis[100]),
                                    SpectralRegion((line_0-3.)*u.Angstrom,(line_0+4.)*u.Angstrom)
                                    ])

    line = (line / g1_fit(x*u.Angstrom))
    return line, header


def resample(spectrum):
    """Return a resampled spectrum with equidistant spectral axis"""
    resampler = LinearInterpolatedResampler(extrapolation_treatment='zero_fill')
    x = np.linspace(sppectrum.spectral_axis[0].value,spectrum.spectral_axis[-1].value,2048)
    return resampler.resample1d(spectrum,x*u.AA)

def save(spectrum,name):
    new_spectrum = Spectrum(xarr=spectrum.spectral_axis, data = spectrum.flux,
                           header=spectrum.header)
    new_spectrum.write(name+'.fits',type='fits')



