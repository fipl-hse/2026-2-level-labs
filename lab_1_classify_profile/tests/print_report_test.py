"""
Checks report printing for detection of language
"""

from pathlib import Path

import pytest
from pytest import CaptureFixture

from lab_1_classify_profile.main import print_report

PATH_TO_ASSETS = Path(__file__).parent / "assets"


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark10
def test_print_report_ideal(capsys: CaptureFixture) -> None:
    """
    Ideal scenario

    Args:
        capsys (CaptureFixture): Pytest fixture to capture output
    """
    profile = (
        "unknown",
        {"happy": 0.2, "man": 0.1},
        2,
    )
    metrics_stats = [
        ("es", {"MSE": 0.0016, "Top-N": 0.2}),
        ("de", {"MSE": 0.0018, "Top-N": 0.4}),
        ("ru", {"MSE": 0.002, "Top-N": 0.4}),
        ("fr", {"MSE": 0.002, "Top-N": 0.2}),
        ("en", {"MSE": 0.0022, "Top-N": 0.22}),
    ]

    assert print_report(profile, metrics_stats, 5) is None
    with open(PATH_TO_ASSETS / "reference_report.txt", "r", encoding="utf-8") as f:
        reference_report = f.read()
    captured = capsys.readouterr()
    assert reference_report == captured.out


@pytest.mark.lab_1_classify_profile
@pytest.mark.mark10
def test_print_report_bad_input(capsys: CaptureFixture) -> None:
    """
    Bad input scenario

    Args:
            capsys (CaptureFixture): Pytest fixture to capture output
    """

    profile = (
        "unknown",
        {"happy": 0.2, "man": 0.1},
        2,
    )
    metrics_stats = [
        ("es", {"MSE": 0.0016, "Top-N": 0.2}),
        ("de", {"MSE": 0.0018, "Top-N": 0.4}),
        ("ru", {"MSE": 0.002, "Top-N": 0.4}),
        ("fr", {"MSE": 0.002, "Top-N": 0.2}),
        ("en", {"MSE": 0.0022, "Top-N": 0.22}),
    ]

    bad_profiles = [3.14, 42, {}, [], (), "string", None]
    bad_metrics = [{"a": "b"}, 42, 3.14, "string", None]
    bad_ns = [{}, set(), (), [], 3.14, "string", None]

    for bad_profile in bad_profiles:
        assert print_report(bad_profile, metrics_stats, 5) is None
        captured = capsys.readouterr()
        assert captured.out == ""

    for bad_metric in bad_metrics:
        assert print_report(profile, bad_metric, 5) is None
        captured = capsys.readouterr()
        assert captured.out == ""

    for bad_n in bad_ns:
        assert print_report(profile, metrics_stats, bad_n) is None
        captured = capsys.readouterr()
        assert captured.out == ""
