import streamlit as st
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

st.set_page_config(page_title="Heart Disease Prediction", page_icon="❤️", layout="centered")

st.markdown(
    """
    <style>
    .main {background-color: #f0f2f6;}
    .stButton>button {background-color: #ff4b4b;}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("❤️ Heart Disease Prediction App")
st.write(
    "Enter your health details below. The app will predict your risk of heart disease using a machine learning model."
)

# Load data and train model (do this only once)
heart_disease = pd.read_csv('heart_disease_data.csv')
X = heart_disease.drop(columns='target', axis=1)
Y = heart_disease['target']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=3)
model = LogisticRegression(max_iter=500)
model.fit(X_train, Y_train)

with st.expander("Personal Information", expanded=True):
    col1, col2 = st.columns(2)
    age = col1.number_input(
        'Age (years)', min_value=1, max_value=100, value=None, format="%d", help="Enter your age (1-100)"
    )
    sex = col2.radio(
        'Sex', ['Male (1)', 'Female (0)'], index=0, help="Male = 1, Female = 0"
    )
    sex_val = 1 if sex.startswith('Male') else 0 if sex.startswith('Female') else None

with st.expander("Medical Details", expanded=True):
    col3, col4 = st.columns(2)
    cp_options = [
        'Select...', 'Typical Angina (0)', 'Atypical Angina (1)', 'Non-anginal Pain (2)', 'Asymptomatic (3)'
    ]
    cp = col3.selectbox(
        'Chest Pain Type', cp_options, index=0,
        help="0: Typical Angina, 1: Atypical Angina, 2: Non-anginal Pain, 3: Asymptomatic"
    )
    cp_val = int(cp.split('(')[-1][0]) if cp != 'Select...' else None
    trestbps = col4.number_input(
        'Resting Blood Pressure (mm Hg)', min_value=80, max_value=200, value=None, format="%d"
    )
    chol = col3.number_input(
        'Serum Cholestoral (mg/dl)', min_value=100, max_value=600, value=None, format="%d"
    )
    fbs = col4.radio(
        'Fasting Blood Sugar > 120 mg/dl', ['Yes (1)', 'No (0)'], index=0, help="Yes = 1, No = 0"
    )
    fbs_val = 1 if fbs.startswith('Yes') else 0 if fbs.startswith('No') else None
    restecg_options = [
        'Select...', 'Normal (0)', 'ST-T Wave Abnormality (1)', 'Left Ventricular Hypertrophy (2)'
    ]
    restecg = col3.selectbox(
        'Resting ECG Results', restecg_options, index=0,
        help="0: Normal, 1: ST-T Wave Abnormality, 2: Left Ventricular Hypertrophy"
    )
    restecg_val = int(restecg.split('(')[-1][0]) if restecg != 'Select...' else None
    thalach = col4.number_input(
        'Max Heart Rate Achieved', min_value=60, max_value=220, value=None, format="%d"
    )
    exang = col3.radio(
        'Exercise Induced Angina', ['Yes (1)', 'No (0)'], index=0, help="Yes = 1, No = 0"
    )
    exang_val = 1 if exang.startswith('Yes') else 0 if exang.startswith('No') else None
    oldpeak = col4.number_input(
        'Oldpeak (ST depression)', min_value=0.0, max_value=10.0, value=None, format="%.2f"
    )
    slope_options = [
        'Select...', 'Upsloping (0)', 'Flat (1)', 'Downsloping (2)'
    ]
    slope = col3.selectbox(
        'Slope of Peak Exercise ST Segment', slope_options, index=0,
        help="0: Upsloping, 1: Flat, 2: Downsloping"
    )
    slope_val = int(slope.split('(')[-1][0]) if slope != 'Select...' else None
    ca = col4.selectbox(
        'Number of Major Vessels Colored by Fluoroscopy', ['Select...', 0, 1, 2, 3], index=0
    )
    ca_val = int(ca) if ca != 'Select...' else None
    thal_options = [
        'Select...', 'Normal (0)', 'Fixed Defect (1)', 'Reversible Defect (2)'
    ]
    thal = col3.selectbox(
        'Thalassemia', thal_options, index=0,
        help="0: Normal, 1: Fixed Defect, 2: Reversible Defect"
    )
    thal_val = int(thal.split('(')[-1][0]) if thal != 'Select...' else None

st.markdown("---")

if st.button('Predict Heart Disease Risk'):
    # Check for missing or out-of-range values
    required_fields = [
        age, sex_val, cp_val, trestbps, chol, fbs_val, restecg_val,
        thalach, exang_val, oldpeak, slope_val, ca_val, thal_val
    ]
    if None in required_fields:
        st.warning("Please fill in all fields with valid values before predicting.")
    else:
        input_data = (
            age, sex_val, cp_val, trestbps, chol, fbs_val, restecg_val,
            thalach, exang_val, oldpeak, slope_val, ca_val, thal_val
        )
        input_data_as_numpy_array = np.asarray(input_data).reshape(1, -1)
        prediction = model.predict(input_data_as_numpy_array)
        if prediction[0] == 0:
            st.success('🎉 The person is unlikely to have Heart Disease.')
        else:
            st.error('⚠️ The person may have Heart Disease. Please consult a doctor.')

        st.write("**Entered Data:**")
        st.json({
            "Age": age,
            "Sex": sex,
            "Chest Pain Type": cp,
            "Resting BP": trestbps,
            "Cholestoral": chol,
            "Fasting Blood Sugar > 120": fbs,
            "Resting ECG": restecg,
            "Max Heart Rate": thalach,
            "Exercise Induced Angina": exang,
            "Oldpeak": oldpeak,
            "Slope": slope,
            "Major Vessels": ca,
            "Thalassemia": thal
        })