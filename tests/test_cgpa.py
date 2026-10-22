import pytest

from src.cgpa import plan_target_cgpa


def test_normal_case():
    # (8.0 * 80 - 7.5 * 60) / 20 = 9.5. Best possible: (450 + 10 * 20) / 80 = 8.125
    result = plan_target_cgpa(7.5, 60, 20, 8.0, max_gpa=10)
    assert result["status"] == "achievable"
    assert result["required_gpa"] == pytest.approx(9.5)
    assert result["max_achievable_cgpa"] == pytest.approx(8.125)


def test_target_already_secured():
    # (8.0 * 110 - 9.0 * 100) / 10 = -2.0, so even a future GPA of 0 is enough
    result = plan_target_cgpa(9.0, 100, 10, 8.0, max_gpa=10)
    assert result["status"] == "already_achieved"
    assert result["required_gpa"] == pytest.approx(-2.0)


def test_impossible_target():
    # (9.0 * 80 - 7.0 * 60) / 20 = 15.0, above the maximum of 10. Best possible: 7.75
    result = plan_target_cgpa(7.0, 60, 20, 9.0, max_gpa=10)
    assert result["status"] == "impossible"
    assert result["required_gpa"] == pytest.approx(15.0)
    assert result["max_achievable_cgpa"] == pytest.approx(7.75)


def test_target_exactly_at_the_limit():
    # The target equals the best possible CGPA, so the required GPA is exactly 10
    result = plan_target_cgpa(7.5, 60, 20, 8.125, max_gpa=10)
    assert result["status"] == "achievable"
    assert result["required_gpa"] == pytest.approx(10.0)


def test_no_future_credits():
    result = plan_target_cgpa(7.5, 60, 0, 8.0, max_gpa=10)
    assert result["status"] == "no_future_credits"
    assert result["required_gpa"] is None
    assert result["max_achievable_cgpa"] == pytest.approx(7.5)


def test_no_completed_credits():
    # A first-semester student: (8.0 * 20 - 0) / 20 = 8.0
    result = plan_target_cgpa(0, 0, 20, 8.0, max_gpa=10)
    assert result["status"] == "achievable"
    assert result["required_gpa"] == pytest.approx(8.0)


def test_four_point_scale():
    # (3.5 * 120 - 3.2 * 90) / 30 = 4.4, above 4.0. Best possible: (288 + 4.0 * 30) / 120 = 3.4
    result = plan_target_cgpa(3.2, 90, 30, 3.5, max_gpa=4.0)
    assert result["status"] == "impossible"
    assert result["required_gpa"] == pytest.approx(4.4)
    assert result["max_achievable_cgpa"] == pytest.approx(3.4)


def test_invalid_inputs_are_rejected():
    with pytest.raises(ValueError):
        plan_target_cgpa(11, 60, 20, 8.0, max_gpa=10)   # CGPA above the scale
    with pytest.raises(ValueError):
        plan_target_cgpa(7.5, -5, 20, 8.0, max_gpa=10)  # negative credits
    with pytest.raises(ValueError):
        plan_target_cgpa(7.5, 60, 20, 12.0, max_gpa=10)  # target above the scale