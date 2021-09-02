from spectools.orbit import *
import pytest
import numpy.testing as npt

JD_phase_EA = [
     [57880.634, 0.0, False],
     [[57924.334,57909.7673,57931.6172], [0.5,0.0,0.75], False],
     [57902.4839, 4.7123, True],
     [57902.4839, 0.75, False],
]

phase_EA=[[
        [0.,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9],
        [0.,1.34412783,1.94137176,2.38774944,2.77593815,3.14159265,3.50724716,3.89543586,4.34181355,4.93905748]]]
@pytest.fixture
def phase_true_anomaly():
    phase = []
    expected_true_anomaly = []
    with open('data/phase-true-anomaly.dat') as f:
       f.readline()
       for line in f:
            p, e = line.split()[0],line.split()[1]
            phase.append(float(p))
            expected_true_anomaly.append(float(e))
    return phase, expected_true_anomaly

@pytest.mark.parametrize("jd,expected_phase,mean_anomaly", JD_phase_EA)
def test_phase(jd, expected_phase, mean_anomaly):
    assert phase(jd, T0=57880.634,P=29.1333,  mean_anomaly=mean_anomaly) == pytest.approx(expected_phase, 0.005)

@pytest.mark.parametrize("phases,expected_mean_anomaly",phase_EA)
def test_excentric_anomaly(phases,expected_mean_anomaly):
    npt.assert_allclose(excentric_anomaly(phases,0.7346),expected_mean_anomaly,rtol=1e-05,atol=1e-06)

def test_true_anomaly(phase_true_anomaly):
    phases,expected_true_anomaly=phase_true_anomaly
    E = excentric_anomaly(phases, e = 0.73462)
    true_anomaly_calculated = true_anomaly(E, e = 0.73462)
    assert true_anomaly_calculated == pytest.approx(expected_true_anomaly,rel=0.1,abs=0.005)
