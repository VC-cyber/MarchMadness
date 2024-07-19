import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import uniform, randint


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

xgb_model = xgb.XGBClassifier(objective='binary:logistic', eval_metric='logloss', 
                              colsample_bytree = 0.8123620356542087, gamma= 0.2852142919229748, 
                              learning_rate= 0.15639878836228102, max_depth= 3, n_estimators= 70, 
                              reg_alpha= 0.07800932022121826, reg_lambda= 0.7339917805043039, 
                              subsample= 0.7174250836504598)


xgb_model.fit(x_train, y_train)

submission_df = pd.read_csv('/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/mens-march-mania-2022/MDataFiles_Stage2/MSampleSubmissionStage2.csv')

submission_df['Pred'] = (xgb_model.predict_proba(x_test))

# Write the predictions to a CSV file
print("Writing predictions to CSV...")
submission_df.to_csv('/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/submission3.csv', index=False)




# param_dist = {
#     'n_estimators': randint(50, 200),
#     'learning_rate': uniform(0.01, 0.2),
#     'max_depth': randint(3, 6),
#     'subsample': uniform(0.7, 0.3),
#     'colsample_bytree': uniform(0.7, 0.3),
#     'gamma': uniform(0, 0.3),
#     'reg_alpha': uniform(0, 0.5),
#     'reg_lambda': uniform(0.5, 1.5)
# }

# # Perform Randomized Search with cross-validation
# random_search = RandomizedSearchCV(estimator=xgb_model, param_distributions=param_dist, 
#                                    scoring='accuracy', n_iter=50, cv=3, verbose=1, random_state=42, n_jobs=-1)
#print("Best parameters found: ", random_search.best_params_)