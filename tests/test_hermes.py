from spectools import hermes
import pytest
from spectools import hermes


@pytest.fixture(scope = 'module')
def open_hermes():
    filename = 'data/hermes_spec.fits'
    return hermes.open(filename)

def test_open(open_hermes):
    spec = open_hermes[0]
    assert len(spec.spectral_axis) == 335536
