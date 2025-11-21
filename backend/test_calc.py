from calculator import calculate_total_score, ask_ai

# Example student data
student_data = {
    'olevel': {'Mathematics':'A*','Physics':'A','Chemistry':'B'},
    'alevel': {'Mathematics':'A','Physics':'B'},
    'alevel_type': 'AS',  # 'AS' or 'Full'
    'matric': 92,
    'fsc': 88,
    'sat': 1450,
    'ecas': [
        {'type':'Academic','ai_points':5},
        {'type':'International','ai_points':3}
    ]
}

total_score = calculate_total_score(student_data)
ai_analysis = ask_ai(student_data)

print("Total Score:", total_score)
print("AI Analysis:", ai_analysis)
