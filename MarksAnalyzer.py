# Student Marks analyzer

import numpy as np

marks = np.array([78, 85, 67, 92, 56, 88, 73, 95, 61, 80])

print("===== STUDENT MARKS ANALYZER =====")

print("Marks:", marks)

print("Highest Marks:", np.max(marks))
print("Lowest Marks:", np.min(marks))
print("Average Marks:", np.mean(marks))
print("Total Marks:", np.sum(marks))

passed = marks[marks >= 40]

print("Number of Students:", len(marks))
print("Students Passed:", len(passed))
print("Students Failed:", len(marks) - len(passed))