import pytest
from spectools.utils import *
import astropy.io.fits as pf
from specutils import Spectrum1D
from numpy.testing import assert_array_equal

def header(filename):
    return pf.getheader(filename)

def test_get_keyword():
    filename = 'data/s1_2016-10-12T04-33-07_ext.fits'
    keyword = get_keyword(header(filename), 'IMFORM')
    assert keyword == 'FITS'

