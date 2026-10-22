"""Target CGPA calculations. There is no Streamlit code here, so this file can be tested on its own."""

TOLERANCE = 1e-9
def validate_inputs(current_cgpa, completed_credits, future_credits, target_cgpa, max_gpa):
    if max_gpa <= 0:
        raise ValueError("The maximum GPA must be greater than 0.")
    if not 0 <= current_cgpa <= max_gpa:
        raise ValueError(f"Current CGPA must be between 0 and {max_gpa:g}.")
    if not 0 <= target_cgpa <= max_gpa:
        raise ValueError(f"Target CGPA must be between 0 and {max_gpa:g}.")
    if completed_credits < 0:
        raise ValueError("Completed credits cannot be negative.")
    if future_credits < 0:
        raise ValueError("Future credits cannot be negative.")
def plan_target_cgpa(current_cgpa, completed_credits, future_credits, target_cgpa, max_gpa=10.0):
    validate_inputs(current_cgpa, completed_credits, future_credits, target_cgpa, max_gpa)

    if future_credits == 0:
        if current_cgpa >= target_cgpa:
            message = f"You have no upcoming credits, so your CGPA stays at {current_cgpa:.2f}, which already meets your target."
        else:
            message = f"You have no upcoming credits, so your CGPA stays at {current_cgpa:.2f}, below your target of {target_cgpa:.2f}. Enter the credits you expect to take."
        return {
            "status": "no_future_credits",
            "required_gpa": None,
            "max_achievable_cgpa": current_cgpa,
            "message": message,
        }

    total_credits = completed_credits + future_credits
    required_gpa = (target_cgpa * total_credits - current_cgpa * completed_credits) / future_credits
    max_achievable = (current_cgpa * completed_credits + max_gpa * future_credits) / total_credits

    if required_gpa <= TOLERANCE:
        status = "already_achieved"
        message = (f"Your target of {target_cgpa:.2f} is already secured. "
                   f"Even a future average of 0 would keep your CGPA at or above it.")
    elif required_gpa > max_gpa + TOLERANCE:
        status = "impossible"
        message = (f"A target of {target_cgpa:.2f} is not possible. Even a perfect {max_gpa:g} "
                   f"in all {future_credits:g} upcoming credits gives a CGPA of {max_achievable:.2f}.")
    else:
        status = "achievable"
        message = (f"You need an average GPA of {required_gpa:.2f} (out of {max_gpa:g}) over your next "
                   f"{future_credits:g} credits to reach a CGPA of {target_cgpa:.2f}.")

    return {
        "status": status,
        "required_gpa": required_gpa,
        "max_achievable_cgpa": max_achievable,
        "message": message,
    }