import pytest
from spectools.utils import *
import astropy.io.fits as pf

@pytest.fixture
def header():
    filename = 'data/s1_2016-10-12T04-33-07_ext.fits'
    return pf.getheader(filename)

def test_get_keyword(header):
    keyword = get_keyword(header, 'IMFORM')
    assert keyword == 'FITS'
