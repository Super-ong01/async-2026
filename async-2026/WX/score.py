import sys
def evaluate_grade(score):
    if score >= 80:
        grade = "Excellent"
    if score >= 50 and score < 80:
        grade = "Pass"
    if score < 50:
        grade = "Fail"
    return grade

def main():
    test_score = 85
    result = evaluate_grade(test_score)
    print(f"Score: {test_score} -> Grade: {result}")

if __name__ == "__main__":
    main()