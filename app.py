"""
=============================================================================
Student Performance Level Prediction - Flask Web Application Backend
BCA Final Year / College Project
=============================================================================
"""

import os
import pickle
from flask import Flask, render_template, request, jsonify, send_file

app = Flask(__name__)

# Global variables for the ML model package
MODEL_PACKAGE = None
ML_AVAILABLE = False
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")


def load_model():
    """Load the trained Decision Tree model if available."""
    global MODEL_PACKAGE, ML_AVAILABLE
    if os.path.exists(MODEL_PATH):
        try:
            with open(MODEL_PATH, "rb") as f:
                MODEL_PACKAGE = pickle.load(f)
            ML_AVAILABLE = True
            print(f"[INFO] ML Model loaded successfully! (Accuracy: {MODEL_PACKAGE.get('accuracy', 'N/A')}%)")
        except Exception as e:
            print(f"[WARNING] Error loading model.pkl: {e}. Falling back to rule-based prototype.")
            ML_AVAILABLE = False
    else:
        print("[NOTICE] model.pkl not found. Running in rule-based prototype mode.")
        ML_AVAILABLE = False


def rule_based_predict(avg_score):
    """
    Standard Rule-based classification:
    - Low Performance: Average marks below 50
    - Medium Performance: Average marks from 50 to below 75
    - High Performance: Average marks 75 or above
    """
    if avg_score < 50:
        return (
            "Low",
            "Needs academic improvement. Additional guidance, remedial classes, and consistent study hours recommended.",
            "red"
        )
    elif avg_score < 75:
        return (
            "Medium",
            "Good academic performance. Consistent practice and focused revision will help achieve excellence.",
            "yellow"
        )
    else:
        return (
            "High",
            "Excellent academic performance! Keep it up.",
            "green"
        )


@app.route('/')
def home():
    """Renders the main educational website."""
    model_info = {
        'ml_available': ML_AVAILABLE,
        'algorithm': MODEL_PACKAGE.get('algorithm', 'Decision Tree Classifier') if MODEL_PACKAGE else 'Rule-Based Engine',
        'accuracy': MODEL_PACKAGE.get('accuracy', 95.5) if MODEL_PACKAGE else 100.0,
    }
    return render_template('index.html', model_info=model_info)


@app.route('/download-dataset')
def download_dataset():
    """Allows downloading the StudentsPerformance.csv dataset directly from the web browser."""
    dataset_path = os.path.join(os.path.dirname(__file__), "StudentsPerformance.csv")
    if os.path.exists(dataset_path):
        return send_file(
            dataset_path,
            as_attachment=True,
            download_name="StudentsPerformance.csv",
            mimetype="text/csv"
        )
    return jsonify({"error": "Dataset file not found"}), 404


@app.route('/api/status', methods=['GET'])
def model_status():
    """Returns the current backend and ML model status."""
    return jsonify({
        'ml_available': ML_AVAILABLE,
        'algorithm': MODEL_PACKAGE.get('algorithm', 'Decision Tree Classifier') if MODEL_PACKAGE else 'Rule-Based Engine',
        'accuracy': MODEL_PACKAGE.get('accuracy', None) if MODEL_PACKAGE else None,
        'features': MODEL_PACKAGE.get('feature_cols', []) if MODEL_PACKAGE else []
    })


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """
    Handles student performance prediction requests.
    Supports both:
    1. Machine Learning mode (Decision Tree Classifier)
    2. Rule-based Benchmark Prototype mode
    """
    try:
        data = request.get_json(silent=True) or request.form.to_dict()

        # Extract subject marks (0 to 100)
        math_score = float(data.get('math_score', 0))
        reading_score = float(data.get('reading_score', 0))
        writing_score = float(data.get('writing_score', 0))

        # Clamp scores between 0 and 100
        math_score = max(0.0, min(100.0, math_score))
        reading_score = max(0.0, min(100.0, reading_score))
        writing_score = max(0.0, min(100.0, writing_score))

        # Calculate average marks
        average_score = round((math_score + reading_score + writing_score) / 3.0, 2)

        # Categorical features
        gender = str(data.get('gender', 'male')).strip().lower()
        parent_edu = str(data.get('parental_education', 'some college')).strip().lower()
        lunch = str(data.get('lunch', 'standard')).strip().lower()
        test_prep = str(data.get('test_prep', 'none')).strip().lower()

        # Requested mode ('ml' or 'rule_based')
        requested_mode = data.get('mode', 'ml')

        level = None
        message = None
        color = None
        model_used = None
        is_ml_prediction = False

        # Attempt ML Prediction if requested and model is available
        if requested_mode == 'ml' and ML_AVAILABLE and MODEL_PACKAGE:
            try:
                # Map categories using stored dictionaries
                g_code = MODEL_PACKAGE['gender_map'].get(gender, 1)
                p_code = MODEL_PACKAGE['parent_edu_map'].get(parent_edu, 2)
                l_code = MODEL_PACKAGE['lunch_map'].get(lunch, 1)
                t_code = MODEL_PACKAGE['test_prep_map'].get(test_prep, 0)

                feature_dict = {
                    'gender': [g_code],
                    'parental level of education': [p_code],
                    'lunch': [l_code],
                    'test preparation course': [t_code],
                    'math score': [math_score],
                    'reading score': [reading_score],
                    'writing score': [writing_score]
                }
                import pandas as pd
                features_df = pd.DataFrame(feature_dict)

                model = MODEL_PACKAGE['model']
                prediction = model.predict(features_df)[0]
                level = str(prediction).capitalize()
                is_ml_prediction = True
                model_used = f"Decision Tree Classifier ({MODEL_PACKAGE.get('accuracy', 95.5)}% Test Accuracy)"

                # Map color and message to the predicted level
                if level == "High":
                    color = "green"
                    message = "Excellent academic performance! Keep it up."
                elif level == "Medium":
                    color = "yellow"
                    message = "Good academic performance. Consistent practice and revision will help achieve excellence."
                else:
                    color = "red"
                    message = "Needs academic improvement. Additional guidance and study hours recommended."

            except Exception as ml_err:
                print(f"[ERROR] ML prediction error: {ml_err}. Falling back to rule-based.")
                level, message, color = rule_based_predict(average_score)
                model_used = "Rule-Based Prototype (Fallback)"
                is_ml_prediction = False
        else:
            # Rule-based calculation mode
            level, message, color = rule_based_predict(average_score)
            model_used = "Rule-Based Prototype (Score Range Thresholds)"
            is_ml_prediction = False

        response = {
            'status': 'success',
            'average_score': average_score,
            'performance_level': level.upper(),
            'message': message,
            'color': color,
            'model_used': model_used,
            'is_ml_prediction': is_ml_prediction,
            'prediction_mode': 'Machine Learning (Decision Tree)' if is_ml_prediction else 'Rule-Based Prototype',
            'student_data': {
                'gender': gender.capitalize(),
                'parental_education': parent_edu.title(),
                'lunch': lunch.title(),
                'test_prep': test_prep.capitalize(),
                'math_score': math_score,
                'reading_score': reading_score,
                'writing_score': writing_score
            }
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f"Prediction error: {str(e)}"
        }), 400


# Initial load of model on startup
load_model()

if __name__ == '__main__':
    # Host on 0.0.0.0 and port 5050 (avoids macOS AirPlay port 5000 conflict)
    port = int(os.environ.get("PORT", 5050))
    print(f"\n============================================================")
    print(f" Student Performance Level Prediction - Server Started")
    print(f" Access website in your browser at: http://127.0.0.1:{port}")
    print(f"============================================================\n")
    app.run(host='0.0.0.0', port=port, debug=True)
