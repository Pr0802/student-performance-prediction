import csv
import random

# Seed for reproducibility
random.seed(42)

genders = ['female', 'male']
race_ethnicities = ['group A', 'group B', 'group C', 'group D', 'group E']
parental_educations = [
    "some high school",
    "high school",
    "some college",
    "associate's degree",
    "bachelor's degree",
    "master's degree"
]
lunch_types = ['standard', 'free/reduced']
test_prep = ['none', 'completed']

rows = []
for i in range(1000):
    gender = random.choice(genders)
    race = random.choice(race_ethnicities)
    parent_edu = random.choices(
        parental_educations,
        weights=[0.18, 0.20, 0.22, 0.22, 0.12, 0.06]
    )[0]
    lunch = random.choices(lunch_types, weights=[0.64, 0.36])[0]
    prep = random.choices(test_prep, weights=[0.65, 0.35])[0]

    # Base academic ability baseline
    base = random.normalvariate(66, 14)
    if lunch == 'standard':
        base += 4
    if prep == 'completed':
        base += 6
    if "master" in parent_edu or "bachelor" in parent_edu:
        base += 4

    # Subject scores with realistic correlation and noise
    math_score = int(min(100, max(15, base + random.normalvariate(0, 7) + (3 if gender == 'male' else -2))))
    reading_score = int(min(100, max(15, base + random.normalvariate(0, 6) + (3 if gender == 'female' else -2))))
    writing_score = int(min(100, max(15, base + random.normalvariate(0, 6) + (4 if gender == 'female' else -3))))

    rows.append([
        gender,
        race,
        parent_edu,
        lunch,
        prep,
        math_score,
        reading_score,
        writing_score
    ])

with open("StudentsPerformance.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "gender",
        "race/ethnicity",
        "parental level of education",
        "lunch",
        "test preparation course",
        "math score",
        "reading score",
        "writing score"
    ])
    writer.writerows(rows)

print("Generated StudentsPerformance.csv with 1000 records successfully!")
