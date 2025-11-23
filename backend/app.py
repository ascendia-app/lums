
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load Excel
file_path = "data/lums_data.xlsx"
programs = pd.read_excel(file_path, sheet_name="programs")
olevel = pd.read_excel(file_path, sheet_name="olevel")
alevel = pd.read_excel(file_path, sheet_name="alevel")
matric = pd.read_excel(file_path, sheet_name="matric")
fsc = pd.read_excel(file_path, sheet_name="fsc")
ecas = pd.read_excel(file_path, sheet_name="ecas")
sat = pd.read_excel(file_path, sheet_name="sat")
points = pd.read_excel(file_path, sheet_name="points")

    
@app.route('/', methods=['GET'])
def home():
    return "Backend working"


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    # extract inputs
    matric_perc = data.get('matric', 0)
    fsc_perc = data.get('fsc', 0)
    sat_score = data.get('sat', 0)
    subjects = data.get('subjects', [])
    ecas_list = data.get('ecas', [])

    # Example: simple calculation (you can replace with your full logic)
    total = matric_perc*0.6 + fsc_perc*0.4 + sat_score*0.03 + len(subjects)*5 + len(ecas_list)*2

    return jsonify({'total_points': total})

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    return jsonify({"total_score": 100, "ai_analysis": "working"})
