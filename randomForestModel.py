import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split

# Load the data 
print("Loading data...")
train_data = pd.read_csv('/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/input_data.csv')
test_data = pd.read_csv('/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/eval_data.csv')
print("Data loaded")

# Split the data into training and testing sets using sklearn
print("Splitting data into training and testing sets...")
x_train, y_train = train_data.drop(['Outcome'], axis=1), train_data['Outcome']
x_test = test_data
#x_train, x_test, y_train, y_test = train_test_split(train_data.drop(['Outcome'], axis=1), train_data['Outcome'], test_size=0.2, random_state=42)
print("Data split")

# Train the model
print("Training models...")

model = RandomForestClassifier(n_estimators=100, random_state=42)

# Fit the model
print("Fitting model...")
model.fit(x_train, y_train)


# Make predictions
print("Making predictions...")

submission_df = pd.read_csv('/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/mens-march-mania-2022/MDataFiles_Stage2/MSampleSubmissionStage2.csv')
print(x_test)
submission_df['Pred'] = (model.predict_proba(x_test))

# Write the predictions to a CSV file
print("Writing predictions to CSV...")
submission_df.to_csv('/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/submission2.csv', index=False)




