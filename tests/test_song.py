from spectools.song import *



def test_extract_line():
    filename = 'data/song_spectrum.fits'
    line,_ = extract_line(filename, 24)
    assert len(line.spectral_axis) == 2048  
    #agregar algún otro despues

# def resampled_spectrum(spectrum)i
# 
#     return equidistant_resample()
# 
# def test_equidist_resample(ResampledSpectrum):
#     expected_delta = (ResampledSpectrum.spectral_axis[-1] -  ResampledSpectrum.spectral_axis[0]) / len(ResampledSpectrum.spectral_axis)
#     assert expected_delta ==
#     ResampledSpectrum.spectral_axis[4]-ResampledSpectrum.spectral_axis[3]
# 
