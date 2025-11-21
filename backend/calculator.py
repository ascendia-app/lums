import pandas as pd

# Load Excel file
file_path = "./data/lums_data.xlsx"
xls = pd.ExcelFile(file_path)

# Load all sheets
programs = pd.read_excel(xls, sheet_name="programs")
olevel = pd.read_excel(xls, sheet_name="olevel")
alevel = pd.read_excel(xls, sheet_name="alevel")
matric = pd.read_excel(xls, sheet_name="matric")
fsc = pd.read_excel(xls, sheet_name="fsc")
ecas = pd.read_excel(xls, sheet_name="ecas")
sat = pd.read_excel(xls, sheet_name="sat")
points = pd.read_excel(xls, sheet_name="points")

# Strip column names to remove accidental spaces
for df in [olevel, alevel, matric, fsc, ecas, sat, points, programs]:
    df.columns = df.columns.str.strip()


# Function to calculate points for O-Level or Matric subjects
def calculate_subject_points(df, student_grades_col='Grade'):
    total = 0
    for idx, row in df.iterrows():
        grade = str(row[student_grades_col]).upper()  # convert to string to avoid float errors
        if grade in ['A*', 'A', 'B', 'C', 'D', 'E']:
            total += row[grade]  # match column name in Excel
        else:
            total += 0
    return total


# Function to calculate A-Level / FSC points considering AS or Full/Internal
def calculate_alevel_points(df, student_grades_dict, level_type='AS'):
    total = 0
    for idx, row in df.iterrows():
        subject = row['Subject']
        grade = student_grades_dict.get(subject, None)
        if not grade:
            continue
        grade = str(grade).upper()
        if grade not in ['A*', 'A', 'B', 'C', 'D', 'E']:
            points_value = 0
        else:
            points_value = row[grade]

        # Adjust for max points based on AS or Full/Internal
        if level_type == 'AS':
            max_points = row['AS Max (Points)']
        else:
            max_points = row['Full A-Level / Internal Max (Points)']

        # Scale points if necessary
        scaled_points = points_value / 5 * max_points  # assuming 5 is max in grade table
        total += scaled_points
    return total


# Function to calculate SAT points
def calculate_sat_points(score):
    # Example: scale SAT to max points from sat sheet
    max_sat_points = sat['Max Points'].iloc[0]  # adjust if multiple rows
    max_score = 1600  # SAT max
    return (score / max_score) * max_sat_points


# Function to calculate ECAs points
def calculate_eca_points(eca_list):
    total = 0
    for eca in eca_list:
        # Here you can integrate AI scoring later
        # For now, sum base points from ecas sheet if matched
        matching = ecas[ecas['Type'].str.lower() == eca['type'].lower()]
        if not matching.empty:
            total += matching['Base Points'].iloc[0]
        # Add extra points if AI text analysis is available
        total += eca.get('ai_points', 0)
    return total


# Full student total score
def calculate_total_score(student_data):
    """
    student_data = {
        'olevel': dict, e.g., {'Mathematics':'A', 'Physics':'B'},
        'alevel': dict, e.g., {'Mathematics':'A*', 'Physics':'A'},
        'alevel_type': 'AS' or 'Full',
        'matric': numeric,
        'fsc': numeric,
        'sat': numeric,
        'ecas': list of dicts, e.g., [{'type':'Academic','ai_points':5}]
    }
    """
    total = 0
    # O-Level points
    olevel_points = 0
    for idx, row in olevel.iterrows():
        subject = row['Subject']
        grade = student_data['olevel'].get(subject, None)
        if grade:
            grade = str(grade).upper()
            if grade in ['A*','A','B','C','D','E']:
                olevel_points += row[grade]
    total += olevel_points * 0.6  # weight 60%

    # A-Level / FSC points
    alevel_points = calculate_alevel_points(alevel, student_data['alevel'], student_data.get('alevel_type','AS'))
    total += alevel_points * 0.4  # weight 40%

    # Matric points
    total += float(student_data.get('matric',0)) * 0.6  # adjust weight

    # FSC points
    total += float(student_data.get('fsc',0)) * 0.4  # adjust weight

    # SAT points
    sat_points = calculate_sat_points(student_data.get('sat',0))
    total += sat_points

    # ECAs points
    eca_points = calculate_eca_points(student_data.get('ecas',[]))
    total += eca_points

    return total


# Stub function for AI analysis (integrate OpenAI later)
def ask_ai(student_data):
    """
    Here you can pass student data to an AI model to categorize ECAs or give admission advice
    """
    return "AI analysis not yet implemented."

