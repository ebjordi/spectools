from spectools.orbit import *
import pytest
import numpy.testing as npt

JD_phase_EA = [
     [55608.63, 0.0, False],
     [[55623.1966,55608.63,55776.1464], [0.5,0.0,0.75], False],
     [55630.47997, 4.7123, True],
     [55630.47997, 0.75, False],
     [55776.1464, 0.75, False]
]

phase_EA=[[
        [0.,0.11111111,0.22222222,0.33333333,0.44444444,0.55555556,0.66666667,0.77777778,0.88888889,0.],
        [1.07319031e-14,1.43090250e+00,2.05216972e+00,2.52332009e+00,2.94040404e+00,3.34278126e+00,3.75986521e+00,4.23101559e+00,4.85228281e+00,5.36595154e-15]]]

@pytest.fixture
def phase_true_anomaly():
    phase = []
    expected_true_anomaly = []
    with open('data/phase-true-anomaly.dat') as f:
        for line in f:
            p, e = line.split()
            phase.append(p)
            expected_true_anomaly.append(e)
    return phase, expected_true_anomaly

@pytest.mark.parametrize("jd,expected_phase,mean_anomaly", JD_phase_EA)
def test_phase(jd, expected_phase, mean_anomaly):
    assert phase(jd, mean_anomaly=mean_anomaly) == pytest.approx(expected_phase, 0.00005)

@pytest.mark.parametrize("phases,expected_mean_anomaly",phase_EA)
def test_excentric_anomaly(phases,expected_mean_anomaly):
    npt.assert_allclose(excentric_anomaly(phases,0.74),expected_mean_anomaly,rtol=1e-05,atol=1e-06)

def test_true_anomaly(phase_true_anomaly):
    phase,expected_true_anomaly=phase_true_anomaly
    E = excentric_anomaly(phase, e = 0.73462)
    true_anomaly_calculated = true_anomaly(E, e = 0.73462)
    np.assert_allclose(true_anomaly_calculated, expected_true_anomaly,
                       atol=1e-03)

