import pytest

from src.exam import contribution, make_assessment, plan_remaining_assessment


def sample_assessments():
    # Assignments: 16 * 20 / 20 = 16 points. Midterm: 42 * 30 / 60 = 21 points. Total earned: 37.
    return [
        make_assessment("Assignments", 16, 20, 20),
        make_assessment("Midterm", 42, 60, 30),
    ]


def test_contribution_is_marks_times_weight_over_max():
    assert contribution(make_assessment("Midterm", 42, 60, 30)) == pytest.approx(21)


def test_make_assessment_cleans_the_name_and_allows_full_and_zero_marks():
    assert make_assessment("  Quiz  ", 10, 10, 5)["name"] == "Quiz"
    assert make_assessment("Quiz", 0, 10, 5)["marks"] == 0


def test_make_assessment_rejects_bad_input():
    with pytest.raises(ValueError):
        make_assessment("  ", 5, 10, 5)      # empty name
    with pytest.raises(ValueError):
        make_assessment("Quiz", 5, 0, 5)     # maximum of 0
    with pytest.raises(ValueError):
        make_assessment("Quiz", 25, 20, 5)   # marks above the maximum
    with pytest.raises(ValueError):
        make_assessment("Quiz", -1, 20, 5)   # negative marks
    with pytest.raises(ValueError):
        make_assessment("Quiz", 5, 10, 0)    # weight of 0


def test_normal_case():
    # Needed: (70 - 37) / 50 = 0.66, so 66%. Out of 80 marks: 33 * 80 / 50 = 52.8
    result = plan_remaining_assessment(sample_assessments(), 50, 70, remaining_max_marks=80)
    assert result["status"] == "achievable"
    assert result["earned_points"] == pytest.approx(37)
    assert result["total_points"] == pytest.approx(100)
    assert result["max_possible_total"] == pytest.approx(87)
    assert result["needed_points"] == pytest.approx(33)
    assert result["needed_percent"] == pytest.approx(66)
    assert result["needed_marks"] == pytest.approx(52.8)


def test_target_already_secured():
    # (30 - 37) * 100 / 50 = -14, so nothing more is needed
    result = plan_remaining_assessment(sample_assessments(), 50, 30)
    assert result["status"] == "already_achieved"
    assert result["needed_percent"] == pytest.approx(-14)


def test_target_exactly_equal_to_points_already_earned():
    result = plan_remaining_assessment(sample_assessments(), 50, 37)
    assert result["status"] == "already_achieved"
    assert result["needed_percent"] == pytest.approx(0)


def test_impossible_target():
    # Needed: (90 - 37) * 100 / 50 = 106%, above the maximum. Best possible total: 87
    result = plan_remaining_assessment(sample_assessments(), 50, 90)
    assert result["status"] == "impossible"
    assert result["needed_percent"] == pytest.approx(106)
    assert result["max_possible_total"] == pytest.approx(87)


def test_target_exactly_at_the_limit():
    # Needed: (87 - 37) * 100 / 50 = 100%, so full marks, which is still achievable
    result = plan_remaining_assessment(sample_assessments(), 50, 87)
    assert result["status"] == "achievable"
    assert result["needed_percent"] == pytest.approx(100)


def test_no_completed_assessments():
    # Nothing done yet: 60 * 100 / 100 = 60%
    result = plan_remaining_assessment([], 100, 60)
    assert result["status"] == "achievable"
    assert result["earned_points"] == 0
    assert result["needed_percent"] == pytest.approx(60)


def test_weights_that_do_not_add_up_to_100():
    # Quiz: 8 * 10 / 10 = 8. Lab: 18 * 15 / 20 = 13.5. Earned: 21.5. Total points: 10 + 15 + 25 = 50
    # Needed for 35: (35 - 21.5) * 100 / 25 = 54%
    assessments = [make_assessment("Quiz", 8, 10, 10), make_assessment("Lab", 18, 20, 15)]
    result = plan_remaining_assessment(assessments, 25, 35)
    assert result["status"] == "achievable"
    assert result["total_points"] == pytest.approx(50)
    assert result["needed_percent"] == pytest.approx(54)


def test_needed_marks_is_none_when_max_marks_not_given():
    result = plan_remaining_assessment(sample_assessments(), 50, 70)
    assert result["needed_marks"] is None


def test_invalid_planner_inputs_are_rejected():
    with pytest.raises(ValueError):
        plan_remaining_assessment(sample_assessments(), 0, 70)                           # remaining weight of 0
    with pytest.raises(ValueError):
        plan_remaining_assessment(sample_assessments(), 50, 101)                         # target above the total of 100
    with pytest.raises(ValueError):
        plan_remaining_assessment(sample_assessments(), 50, -1)                          # negative target
    with pytest.raises(ValueError):
        plan_remaining_assessment(sample_assessments(), 50, 70, remaining_max_marks=0)   # maximum marks of 0

