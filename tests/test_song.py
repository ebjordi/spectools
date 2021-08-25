from spectools.song import *
import pytest
from specutils import Spectrum1D

@pytest.fixture
def song_spectrum():
    filename = 'data/song_spectrum.fits'
    return extract_line(filename, 24)

def test_extract_line(song_spectrum):
    assert len(song_spectrum[0].spectral_axis) == 2048
    #agregar algún otro despues

def test_equidist_resample(song_spectrum):
    resampled_spectrum = equidistant_resample(song_spectrum[0])
    expected_delta = (song_spectrum[0].spectral_axis[-1] -
                      song_spectrum[0].spectral_axis[0]) / len(song_spectrum[0].spectral_axis)
    delta = resampled_spectrum.spectral_axis.value[1:] - resampled_spectrum.spectral_axis.value[:-1]
    assert delta.all == expected_delta.value

