"""Reply Policy"""
def explain_cannot_with_fix(reason, solution):
    return f"Ben yapamıyorum çünkü {reason}. Eğer benim yapmamı istiyorsan {solution}."

def success_with_details(action, details=""):
    result = f"✅ {action}"
    if details:
        result += f"\n{details}"
    return result
