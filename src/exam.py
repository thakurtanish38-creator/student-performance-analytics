"""Internal and final exam calculations. There is no Streamlit code here, so this file can be tested on its own."""

TOLERANCE = 1e-9


def make_assessment(name, marks, max_marks, weight):
    name = name.strip()
    if not name:
        raise ValueError("Each assessment needs a name.")
    if max_marks <= 0:
        raise ValueError(f"'{name}': the maximum marks must be greater than 0.")
    if marks < 0 or marks > max_marks:
        raise ValueError(f"'{name}': the marks must be between 0 and {max_marks:g}.")
    if weight <= 0:
        raise ValueError(f"'{name}': the weight must be greater than 0.")
    return {"name": name, "marks": marks, "max_marks": max_marks, "weight": weight}
def contribution(assessment):
    return assessment["marks"] * assessment["weight"] / assessment["max_marks"]
def plan_remaining_assessment(assessments, remaining_weight, target_total, remaining_max_marks=None):
    if remaining_weight <= 0:
        raise ValueError("The weight of the remaining assessment must be greater than 0.")
    if remaining_max_marks is not None and remaining_max_marks <= 0:
        raise ValueError("The maximum marks of the remaining assessment must be greater than 0.")

    earned_points = sum(contribution(item) for item in assessments)
    completed_weight = sum(item["weight"] for item in assessments)
    total_points = completed_weight + remaining_weight

    if not 0 <= target_total <= total_points:
        raise ValueError(f"The target must be between 0 and {total_points:g}, the total of all the weights.")

    max_possible_total = earned_points + remaining_weight
    needed_points = target_total - earned_points
    needed_percent = needed_points * 100 / remaining_weight
    needed_marks = None
    if remaining_max_marks is not None:
        needed_marks = needed_points * remaining_max_marks / remaining_weight

    if needed_points <= TOLERANCE:
        status = "already_achieved"
        message = (f"Your target of {target_total:g} is already secured: you already have "
                   f"{earned_points:g} points before the remaining assessment.")
    elif needed_percent > 100 + TOLERANCE:
        status = "impossible"
        message = (f"A target of {target_total:g} is not possible. Even full marks in the remaining "
                   f"assessment would give {max_possible_total:g} out of {total_points:g}.")
    else:
        status = "achievable"
        message = (f"You need {needed_percent:.1f}% in the remaining assessment "
                   f"({needed_points:g} of its {remaining_weight:g} points)")
        if needed_marks is not None:
            message += f", which is {needed_marks:.1f} out of {remaining_max_marks:g} marks"
        message += f", to reach a total of {target_total:g}."

    return {
        "status": status,
        "earned_points": earned_points,
        "total_points": total_points,
        "max_possible_total": max_possible_total,
        "needed_points": needed_points,
        "needed_percent": needed_percent,
        "needed_marks": needed_marks,
        "message": message,
    }
