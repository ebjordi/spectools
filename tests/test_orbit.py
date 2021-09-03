from spectools.orbit import *
import pytest
import numpy.testing as npt

JD_phase_EA = [
     [57880.634, 0.0, False],
     [[57924.334,57909.7673,57931.6172], [0.5,0.0,0.75], False],
     [57902.4839, 4.7123, True],
     [57902.4839, 0.75, False],
]

phase_EA_TA=[[
        [0.,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9],
        [0.,1.34412783,1.94137176,2.38774944,2.77593815,3.14159265,3.50724716,3.89543586,4.34181355,4.93905748],
        [0.0,2.22772102,2.61851838,2.83435559,2.99720062,3.14159265,3.28598469,3.44882972,3.66466693,4.05546429]]]

@pytest.mark.parametrize("jd,expected_phase,mean_anomaly", JD_phase_EA)
def test_phase(jd, expected_phase, mean_anomaly):
    assert phase(jd, T0=57880.634,P=29.1333,  mean_anomaly=mean_anomaly) == pytest.approx(expected_phase, 0.005)

@pytest.mark.parametrize("phases,expected_e_anomaly,t",phase_EA_TA)
def test_excentric_anomaly(phases,expected_e_anomaly,t):
    npt.assert_allclose(excentric_anomaly(phases,0.7346),expected_e_anomaly,rtol=1e-05,atol=1e-06)

@pytest.mark.parametrize("ph,expected_EA,expected_TA",phase_EA_TA)
def test_true_anomaly(ph,expected_EA,expected_TA):
    true_anomaly_calculated = true_anomaly(expected_EA, e = 0.73462)
    assert true_anomaly_calculated == pytest.approx(expected_TA,0.005)
