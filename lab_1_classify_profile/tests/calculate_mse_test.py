"""
Checks the first lab calculation of the mean squared error function
"""

import pytest

from admin_utils.constants import FLOAT_TOLERANCE
from lab_1_classify_profile.main import calculate_mse


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark8
@pytest.mark.mark10
def test_calculate_mse_ideal() -> None:
    """
    Ideal scenario
    """
    predicted_value = [
        0.1538,
        0.0,
        0.0,
        0.0769,
        0.0769,
        0.0769,
        0.0,
        0.0,
        0.0769,
        0.0769,
        0.0769,
        0.1538,
        0.2307,
        0.0,
    ]

    actual_value = [
        0.1666,
        0.1666,
        0.0333,
        0.1333,
        0.0,
        0.0666,
        0.0666,
        0.0333,
        0.0333,
        0.1,
        0.0666,
        0.0,
        0.0666,
        0.0666,
    ]

    expected = 0.0072
    actual = calculate_mse(predicted_value, actual_value)
    assert expected == pytest.approx(actual, abs=FLOAT_TOLERANCE)


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark8
@pytest.mark.mark10
def test_calculate_mse_bad_input_length() -> None:
    """
    Bad input scenario
    """
    predicted_value = [
        0.1538,
        0.0,
        0.0,
        0.0769,
        0.0769,
        0.0769,
        0.0,
        0.0,
        0.0769,
        0.0769,
        0.0769,
        0.1538,
        0.2307,
        0.0,
    ]

    actual_value = [0.1666, 0.1666, 0.0333, 0.1333, 0.0, 0.0666, 0.0666, 0.0333, 0.0333, 0.1]

    expected = None
    actual = calculate_mse(predicted_value, actual_value)
    assert expected == actual


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark8
@pytest.mark.mark10
def test_calculate_mse_bad_input_predicted() -> None:
    """
    Bad input scenario
    """
    predicted_value = "0.0"

    actual_value = [
        0.1666,
        0.1666,
        0.0333,
        0.1333,
        0.0,
        0.0666,
        0.0666,
        0.0333,
        0.0333,
        0.1,
        0.0666,
        0.0,
        0.0666,
        0.0666,
    ]

    expected = None
    actual = calculate_mse(predicted_value, actual_value)
    assert expected == actual


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark8
@pytest.mark.mark10
def test_calculate_mse_bad_input_actual() -> None:
    """
    Bad input scenario
    """
    predicted_value = [
        0.1538,
        0.0,
        0.0,
        0.0769,
        0.0769,
        0.0769,
        0.0,
        0.0,
        0.0769,
        0.0769,
        0.0769,
        0.1538,
        0.2307,
        0.0,
    ]

    actual_value = {}

    expected = None
    actual = calculate_mse(predicted_value, actual_value)
    assert expected == actual
