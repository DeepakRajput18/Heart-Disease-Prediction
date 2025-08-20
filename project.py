
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


heart_disease = pd.read_csv('heart_disease_data.csv')
print(heart_disease.head(), '\n')
print(heart_disease.shape, '\n')
print(heart_disease.describe(), '\n')
print(heart_disease.info(), '\n')


# Checking the missing values -
print(heart_disease.isnull().sum(), '\n')


# Checking the distribution of Target Variable -
print(heart_disease['target'].value_counts(), '\n')                             # 1 represent Defective Heart and 0 represent Healthy Heart.


# Splitting the features and Target -

X = heart_disease.drop(columns='target', axis=1)
Y = heart_disease['target']
print(X, '\n')
print(Y, '\n')


# Splitting the Data into Training Data and Testing Data -

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=3)
print(X.shape, X_train.shape, X_test.shape, '\n')
print(Y.shape, Y_train.shape, Y_test.shape, '\n')


# MODEL TRAINING :-

# Logistic Regression -
model = LogisticRegression()

# Training the LogisticRegression Model with Training Data -
model.fit(X_train, Y_train)


# MODEL EVALUATION :-

# ACCURANCY SCORE :-
# Accurancy on Training Data -
X_train_prediction = model.predict(X_train)
Training_data_accurancy = accuracy_score(X_train_prediction, Y_train)
print('Accurancy on Training Data : ', Training_data_accurancy, '\n')

# Accurancy on Testing Data -
X_test_prediction = model.predict(X_test)
Testing_data_accurancy = accuracy_score(X_test_prediction, Y_test)
print('Accurancy on Testing Data : ', Testing_data_accurancy, '\n')


# BUILDING A PREDICTIVE DATA  :-

input_data = (54,1,0,140,239,0,1,160,0,1.2,2,0,2)

# Change the input data to a numpy array -
input_data_as_numpy_array = np.asarray(input_data)

# Reshape the Numpy array as we are predicting for only on instance -
input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
prediction = model.predict(input_data_reshaped)
print(prediction, '\n')

if (prediction[0] == 0):
    print('The person does not have a Heart Disease')
else:
    print('The person has Heart Disease')

