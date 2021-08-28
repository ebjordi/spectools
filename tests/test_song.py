from spectools.song import *
import pytest
from specutils import Spectrum1D
from numpy.testing import assert_allclose
import os

@pytest.fixture(scope='module')
def song_spectrum():
    filename = 'data/song_spectrum.fits'
    return extract_line(filename, 24)

@pytest.fixture
def equidistant_spectrum(song_spectrum):
    return equidistant_resample(song_spectrum[0])

def test_extract_line(song_spectrum):
    assert len(song_spectrum[0].spectral_axis) == 2048
    #agregar algún otro despues

def test_equidistant_resample(equidistant_spectrum):
    delta = equidistant_spectrum.spectral_axis.value[1:] - equidistant_spectrum.spectral_axis.value[:-1]
    assert_allclose(delta[1:-1],delta[2])

def test_save(song_spectrum, equidistant_spectrum):
    filename = 'data/test_save.fits'
    if os.path.exists(filename):
        os.remove(filename)
    save(equidistant_spectrum, filename, song_spectrum[1])
    assert os.path.getsize(filename) > 0
