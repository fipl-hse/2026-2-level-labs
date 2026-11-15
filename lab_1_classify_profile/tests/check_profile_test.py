"""
Checks report printing for detection of language
"""

import pytest

from lab_1_classify_profile.main import check_profile


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_check_profile_ideal() -> None:
    """
    Ideal scenario
    """
    profile = ("unknown", {"happy": 0.2, "man": 0.1}, 2)

    assert check_profile(profile) is True


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
def test_check_profile_bad_input() -> None:
    """
    Bad input scenario
    """
    bad_profiles = [
        3.14,
        42,
        [],
        (),
        "string",
        None,
        {},
        ("name", {"freq": 1.0}, 1, 0),
        ("name", {"freq": 1.0}, "n_words"),
        ("name", {"freq": "1.0"}, 1),
        ("name", {0: 1.0}, 1),
        (None, {"freq": 1.0}, 1),
    ]

    for bad_profile in bad_profiles:
        assert check_profile(bad_profile) is False
