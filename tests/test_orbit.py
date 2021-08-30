from spectools.orbit import *
import pytest

JD = [
     [2455608.29, 0.0, False],
     [[2455622.8575,2455608.29,2455775.81625], [0.5,0.0,0.75], False],
     [2455630.14125, 4.7123, True],
     [2455630.14125, 0.75, False],
     [2455775.81625, 0.75, False]
]

@pytest.mark.parametrize("hjd,expected_phase,mean_anomaly", JD)
def test_phase(hjd, expected_phase, mean_anomaly):
    assert phase(hjd, mean_anomaly=mean_anomaly) == pytest.approx(expected_phase, 0.00005)
