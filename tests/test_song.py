from spectools.song import *
import pytest
from specutils import Spectrum1D

# @pytest.fixture
#def non_resampled_spectrum():
#    filename = 'data/song_order-no-resample.fits'
#    return Spectrum1D.read(filename)

@pytest.fixture
def song_spectrum():
    filename = 'data/song_spectrum.fits'
    return extract_line(filename, 24)

def test_extract_line(song_spectrum):
    assert len(song_spectrum[0].spectral_axis) == 2048
    #agregar algún otro despues

#def test_equidist_resample(non_resampled_spectrum):
#    resampled_spectrum = equidistant_resample(non_resampled_spectrum)
#    expected_delta = (resampled_spectrum.spectral_axis[-1] - resampled_spectrum.spectral_axis[0]) / len(resampled_spectrum.spectral_axis)
#    delta = resampled_spectrum.spectral_axis.value[1:] - resampled_spectrum.spectral_axis.value[:-1]
 #   assert resampled_spectrum.spectral_axis.value.all == expected_delta
#     ResampledSpectrum.spectral_axis[4]-ResampledSpectrum.spectral_axis[3]
# 
