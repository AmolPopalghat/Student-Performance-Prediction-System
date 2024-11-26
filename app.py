from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load the saved model and scaler
svm_model = joblib.load('svm_model.pkl')
scaler = joblib.load('scaler.pkl')

# Home route to display the form
@app.route('/')
def index():
    return render_template('index.html')

# Prediction route to handle user input and model prediction
@app.route('/predict', methods=['POST'])
def predict():
    # Get data from the HTML form
    data = request.get_json()

    # Extracting features from the input data
    hours_studied = float(data['Hours_Studied'])
    attendance = float(data['Attendance'])
    previous_scores = float(data['Previous_Scores'])
    sleep_hours = float(data['Sleep_Hours'])
    motivation_level = data['Motivation_Level']

    # Map motivation level to a numeric value
    motivation_map = {'Low': 0, 'Medium': 1, 'High': 2}
    motivation_level = motivation_map.get(motivation_level, 0)

    # Prepare input data
    input_features = np.array([[hours_studied, attendance, previous_scores, sleep_hours, motivation_level]])

    # Scale the input features using the pre-trained scaler
    input_features_scaled = scaler.transform(input_features)

    # Make the prediction using the SVM model
    predicted_score = svm_model.predict(input_features_scaled)

    # Return the prediction as a JSON response
    return jsonify({'Exam_Score': predicted_score[0]})

if __name__ == '__main__':
    app.run(debug=True)
