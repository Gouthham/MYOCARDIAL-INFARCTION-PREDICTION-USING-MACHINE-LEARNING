import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import csv

# Function to train and save the model
def train_and_save_model():
    # Load your dataset
    data = pd.read_csv(r"C:\Users\rsrip\Desktop\miniproject (3)\miniproject (2)\miniproject\Heart.csv")

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

# Function to load the model and make predictions
def random_forest_pred(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal):
    # Load the trained model from pickle file
    with open('random_forest_model.pkl', 'rb') as model_file:
        clf = pickle.load(model_file)
    
    # Prepare new data for prediction
    new_data = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
    
    # Make predictions
    result = clf.predict([new_data])[0]
    
    # Write to CSV file
    with open("heart.csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, result])
    
    return result

# Call the function to train and save the model (only once)
train_and_save_model()

# Example usage
age = 71
sex = 0  # Assuming Male (1) based on your previous implementation
cp = 0   # Assuming Typical Angina (0) based on your previous implementation
trestbps = 112
chol = 149
fbs = 0  # Assuming No (0) for Fasting Blood Sugar based on your previous implementation
restecg = 1  # Assuming Normal (0) for Resting Electrocardiographic Results based on your previous implementation
thalach = 125
exang = 0 # Assuming Yes (1) for Exercise Induced Angina based on your previous implementation
oldpeak = 1.6
slope = 1  # Assuming Downsloping (2) for Slope based on your previous implementation
ca = 0
thal = 2   # Assuming Reversible Defect (3) for Thalassemia based on your previous implementation

# Call the function to make a prediction
prediction = random_forest_pred(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal)

print("Prediction:", prediction)
