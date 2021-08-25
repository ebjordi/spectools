from spectools.song import *
import pytest
from specutils import Spectrum1D
from numpy.testing import assert_allclose

@pytest.fixture
def song_spectrum():
    filename = 'data/song_spectrum.fits'
    return extract_line(filename, 24)

def test_extract_line(song_spectrum):
    assert len(song_spectrum[0].spectral_axis) == 2048
    #agregar algún otro despues

def test_equidist_resample(song_spectrum):
    resampled_spectrum = equidistant_resample(song_spectrum[0])
    delta = resampled_spectrum.spectral_axis.value[1:] - resampled_spectrum.spectral_axis.value[:-1]
    assert_allclose(delta[1:-1],delta[2])

