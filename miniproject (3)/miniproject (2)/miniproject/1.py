import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import csv

def random_forest_pred(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal):
    # Load your dataset
    data = pd.read_csv("heart.csv")
    
    # Split dataset into features (X) and target (y)
    X = data.drop('target', axis=1)
    y = data['target']
    
    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=109)
    
    # Initialize RandomForestClassifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # Train the classifier
    clf.fit(X_train, y_train)
    
    # Prepare new data for prediction
    new_data = [[38,1,2,138,175,0,1,173,0,0,2,4,2], [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]]
    
    # Make predictions
    result = clf.predict([new_data[1]])[0]  # Predict for the second row in new_data
    
    # Write to CSV file
    with open("heart.csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, result])
    
    return result
