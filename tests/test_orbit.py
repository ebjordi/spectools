from spectools.orbit import *
import pytest
import numpy.testing as npt

JD_phase_EA = [
     [2455608.29, 0.0, False],
     [[2455622.8575,2455608.29,2455775.81625], [0.5,0.0,0.75], False],
     [2455630.14125, 4.7123, True],
     [2455630.14125, 0.75, False],
     [2455775.81625, 0.75, False]
]

phase_EA=[[
        [0.,0.11111111,0.22222222,0.33333333,0.44444444,0.55555556,0.66666667,0.77777778,0.88888889,0.],
        [1.07319031e-14,1.43090250e+00,2.05216972e+00,2.52332009e+00,2.94040404e+00,3.34278126e+00,3.75986521e+00,4.23101559e+00,4.85228281e+00,5.36595154e-15]]]

@pytest.mark.parametrize("jd,expected_phase,mean_anomaly", JD_phase_EA)
def test_phase(jd, expected_phase, mean_anomaly):
    assert phase(jd, mean_anomaly=mean_anomaly) == pytest.approx(expected_phase, 0.00005)

@pytest.mark.parametrize("phases,expected_mean_anomaly",phase_EA)
def test_excentric_anomaly(phases,expected_mean_anomaly):
    npt.assert_allclose(excentric_anomaly(phases,0.74),expected_mean_anomaly,rtol=1e-05,atol=1e-06)

