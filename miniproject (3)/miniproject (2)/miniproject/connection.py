from flask import Flask, render_template, request, jsonify
import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

app = Flask(__name__)

# Global variables for storing user information
speech, name, age1, gender = "", "", "", ""
problem, sym_duration = "", ""
q1, q2, q3, q4, q5, q6 = 0, 0, 0, 0, 0, 0
sym1, sym2, sym3 = "", "", ""
new_report, tips, soln = "", "", ""
doctor, date, time = "", "", ""

# Mapping categorical values to numeric values
cp_mapping = {
    'Typical Angina': 0,
    'Atypical Angina': 1,
    'Non-anginal Pain': 2,
    'Asymptomatic': 3
}
restecg_mapping = {
    'Normal': 0,
    'Having ST-T wave abnormality': 1,
    'Left ventricular hypertrophy': 2
}
slope_mapping = {
    'Upsloping': 0,
    'Flat': 1,
    'Downsloping': 2
}
ca_mapping = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4
}
thal_mapping = {
    'Normal': 1,
    'Fixed Defect': 2,
    'Reversible Defect': 3
}

# Convert 'Yes'/'No' to numeric
yes_no_mapping = {
    'Yes': 1,
    'No': 0
}

@app.route('/home')
def Home():
    return render_template('home.html')

@app.route('/about')
def pass_page():
    return render_template('about.html')
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')



@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/', methods=['GET', 'POST'])
def getvalue():
    if request.method == 'POST':
        try:
            # Extracting form data and converting to appropriate types
            age1 = int(request.form.get('age'))
            gender = request.form.get('sex')
            cp = cp_mapping.get(request.form.get('cp'))
            trestbps = float(request.form.get('trestbps'))
            chol = float(request.form.get('chol'))
            fbs = yes_no_mapping.get(request.form.get('fbs'))
            restecg = restecg_mapping.get(request.form.get('restecg'))
            thalach = float(request.form.get('thalach'))
            exang = yes_no_mapping.get(request.form.get('exang'))
            oldpeak = float(request.form.get('oldpeak'))
            slope = slope_mapping.get(request.form.get('slope'))
            ca = ca_mapping.get(request.form.get('ca'))
            thal = thal_mapping.get(request.form.get('thal'))

            # Convert gender to numeric value
            gender_numeric = 1 if gender.lower() == 'male' else 0

            try:
                # Get the prediction
                op = random_forest_pred(age1, gender_numeric, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal)
                print(f"Prediction: {op}")  # Print the prediction to console/log
            except Exception as e:
                print(f"Prediction error: {e}")
                return "Error occurred during prediction: " + str(e)

            # Determine result string based on prediction
            if op == 0:
                opstr = "No Heart Disease"
                speech = "Your report looks fine."
            elif op == 1:
                opstr = "Heart Disease Present"
                speech = "You may be suffering from a heart disease/problem!"

            # Render the form page with prediction result and form data
            return render_template('form.html', prediction=opstr, name=request.form.get('name'), age=age1, sex=gender,
                                   cp=request.form.get('cp'), trestbps=trestbps, chol=chol, fbs=request.form.get('fbs'),
                                   restecg=request.form.get('restecg'), thalach=thalach, exang=request.form.get('exang'),
                                   oldpeak=oldpeak, slope=request.form.get('slope'), ca=request.form.get('ca'),
                                   thal=request.form.get('thal'))
        except ValueError as e:
            print(f"ValueError: {e}")
            return "Invalid input values. Please check your input."
    else:
        # Handle GET request for homepage or other methods
        return render_template('home.html')




@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = makeWebhookResult(req)
    res = jsonify(res)  # Convert dictionary to JSON response
    return res

def makeWebhookResult(req):
    query_response = req.get("queryResult", {})
    fulfillment_text = ""

    global name, gender, age1, sym1, sym2, new_report

    if query_response.get("action") == "user_name":
        name = query_response.get("parameters", {}).get("given-name")
    
    if query_response.get("action") == "user_age":
        age1 = int(query_response.get("parameters", {}).get("age", {}).get("amount", 0))
    
    if query_response.get("action") == "DefaultWelcomeIntent.DefaultWelcomeIntent-custom.Checkup_Patient-custom":
        gender = query_response.get("parameters", {}).get("Gender")
        fulfillment_text = f"OK {name} ({age1}), please fill and submit the report form on the right side."

    return {"fulfillmentText": fulfillment_text}

def random_forest_pred(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal):
    # Load the trained model from pickle file
    with open('random_forest_model.pkl', 'rb') as model_file:
        clf = pickle.load(model_file)
    
    # Prepare new data for prediction
    input_data = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
    
    # Make prediction
    prediction = clf.predict(input_data)
    return prediction[0]

if __name__ == '__main__':
    # Train and save the model (uncomment if you need to retrain the model)
    '''
    def train_and_save_model():
        # Load your dataset
        data = pd.read_csv("heart.csv")

        # Split dataset into features (X) and target (y)
        X = data.drop('TARGET', axis=1)
        y = data['TARGET']

        # Split data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=109)

        # Initialize RandomForestClassifier
        clf = RandomForestClassifier(n_estimators=100, random_state=42)

        # Train the classifier
        clf.fit(X_train, y_train)

        # Save the trained model to a pickle file
        with open('random_forest_model.pkl', 'wb') as model_file:
            pickle.dump(clf, model_file)
    
    # Uncomment the following line if you need to retrain the model
    # train_and_save_model()
    '''
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, port=port, host='0.0.0.0')
