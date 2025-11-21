from flask import Flask, request, render_template
import pandas as pd
from calculator import calculate_total_score, ask_ai

app = Flask(__name__, template_folder='../frontend')  # point to frontend folder

@app.route('/')
def home():
    return render_template('index.html')  # loads frontend/index.html

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.form
    # parse grades and numbers from form
    total_score = calculate_total_score(data)
    ai_analysis = ask_ai(data)  # optional AI analysis
    return render_template('result.html', score=total_score, analysis=ai_analysis)

if __name__ == '__main__':
    app.run(debug=True)
