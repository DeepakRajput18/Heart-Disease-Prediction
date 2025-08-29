import streamlit as st
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

st.set_page_config(page_title="Heart Disease Prediction", page_icon="❤️", layout="wide")

st.markdown(
    """
    <style>
    .main {background-color: #f0f2f6;}
    .stButton>button {background-color: #ff4b4b;}
    .big-title {font-size: 3em !important; font-weight: bold;}
    .info-box {
        background: #23272f;  /* dark background */
        color: #f0f2f6;       /* light text */
        border-radius: 8px;
        padding: 1em;
        margin-bottom: 1em;
        font-size: 1.15em;
    }
    .result-box {background: #d1e7dd; border-radius: 8px; padding: 1em; margin-top: 1em;}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="big-title">❤️ Heart Disease Prediction App</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="info-box">
    Welcome to the Heart Disease Prediction App!<br>
    This tool uses a machine learning model trained on medical data to estimate your risk of heart disease.<br>
    <b>How to use:</b> Fill in your health details below. Each field includes a description to help you.<br>
    <b>Disclaimer:</b> This app is for educational purposes only. For medical advice, consult a healthcare professional.
    </div>
    """,
    unsafe_allow_html=True
)

# Load data and train model (do this only once)
heart_disease = pd.read_csv('heart_disease_data.csv')
X = heart_disease.drop(columns='target', axis=1)
Y = heart_disease['target']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=3)
model = LogisticRegression(max_iter=500)
model.fit(X_train, Y_train)

with st.expander("Personal Information", expanded=True):
    col1, col2, col3 = st.columns([1,1,1])
    age = col1.number_input(
        'Age (years)', min_value=1, max_value=100, value=None, format="%d",
        help="Your age in years (1-100)."
    )
    sex = col2.radio(
        'Gender', ['Male', 'Female'], index=0,
        help="Select your biological sex. Male = 1, Female = 0."
    )
    sex_val = 1 if sex.startswith('Male') else 0 if sex.startswith('Female') else None
    thalach = col3.number_input(
        'Max Heart Rate Achieved', min_value=60, max_value=220, value=None, format="%d",
        help="Maximum heart rate achieved during exercise (60-220 bpm)."
    )

with st.expander("Medical Details", expanded=True):
    col4, col5, col6 = st.columns([1,1,1])
    cp_mapping = {
        'Typical Angina': 0,
        'Atypical Angina': 1,
        'Non-anginal Pain': 2,
        'Asymptomatic': 3
    }
    cp_options = ['Select...'] + list(cp_mapping.keys())
    cp = col4.selectbox(
        'Chest Pain Type', cp_options, index=0,
        help="Type of chest pain: 0=Typical Angina, 1=Atypical Angina, 2=Non-anginal Pain, 3=Asymptomatic."
    )
    cp_val = cp_mapping.get(cp) if cp in cp_mapping else None

    trestbps = col5.number_input(
        'Resting Blood Pressure (mm Hg)', min_value=80, max_value=200, value=None, format="%d",
        help="Resting blood pressure in mm Hg (80-200)."
    )
    chol = col6.number_input(
        'Serum Cholestoral (mg/dl)', min_value=100, max_value=600, value=None, format="%d",
        help="Serum cholesterol in mg/dl (100-600)."
    )

    fbs = col4.radio(
        'Fasting Blood Sugar > 120 mg/dl', ['Yes', 'No'], index=0,
        help="Is fasting blood sugar > 120 mg/dl? Yes = 1, No = 0."
    )
    fbs_val = 1 if fbs.startswith('Yes') else 0 if fbs.startswith('No') else None

    restecg_options = [
    'Select...', 'Normal', 'ST-T Wave Abnormality', 'Left Ventricular Hypertrophy'
]
restecg = col5.selectbox(
    'Resting ECG Results', restecg_options, index=0,
    help="Resting ECG: 0=Normal, 1=ST-T Wave Abnormality, 2=Left Ventricular Hypertrophy."
)
restecg_val = None
if restecg != 'Select...':
    restecg_val = int(restecg.split('-')[-1].strip())

exang = col6.radio(
    'Exercise Induced Angina', ['Yes', 'No'], index=0,
    help="Did you experience angina during exercise? Yes = 1, No = 0."
)
exang_val = 1 if exang.startswith('Yes') else 0 if exang.startswith('No') else None

oldpeak = col4.number_input(
    'Oldpeak (ST depression)', min_value=0.0, max_value=10.0, value=None, format="%.2f",
    help="ST depression induced by exercise relative to rest (0.0-10.0)."
)

slope_options = [
    'Select...', 'Upsloping', 'Flat', 'Downsloping'
]
slope = col5.selectbox(
    'Slope of Peak Exercise ST Segment', slope_options, index=0,
    help="Slope of the peak exercise ST segment: 0=Upsloping, 1=Flat, 2=Downsloping."
)
slope_val = None
if slope != 'Select...':
    slope_val = int(slope.split('-')[-1].strip())


    ca = col6.selectbox(
        'Number of Major Vessels Colored by Fluoroscopy', ['Select...', 0, 1, 2, 3], index=0,
        help="Number of major vessels (0-3) colored by fluoroscopy."
    )
    ca_val = int(ca) if ca != 'Select...' else None

    thal_mapping = {
    'Normal': 0,
    'Fixed Defect': 1,
    'Reversible Defect': 2
}

thal_options = ['Select...'] + list(thal_mapping.keys())
thal = col4.selectbox(
    'Thalassemia', thal_options, index=0,
    help="Thalassemia type: 0=Normal, 1=Fixed Defect, 2=Reversible Defect."
)
thal_val = thal_mapping.get(thal) if thal in thal_mapping else None


st.markdown("---")

with st.expander("Feature Information", expanded=False):
    st.markdown("""
    - **Age:** Age in years.
    - **Sex:** Male (1), Female (0).
    - **Chest Pain Type:** 0=Typical Angina, 1=Atypical Angina, 2=Non-anginal Pain, 3=Asymptomatic.
    - **Resting Blood Pressure:** Measured in mm Hg.
    - **Serum Cholestoral:** Measured in mg/dl.
    - **Fasting Blood Sugar:** >120 mg/dl (1=True, 0=False).
    - **Resting ECG:** 0=Normal, 1=ST-T Wave Abnormality, 2=Left Ventricular Hypertrophy.
    - **Max Heart Rate Achieved:** During exercise.
    - **Exercise Induced Angina:** 1=Yes, 0=No.
    - **Oldpeak:** ST depression induced by exercise.
    - **Slope:** Slope of peak exercise ST segment.
    - **Major Vessels:** Number colored by fluoroscopy (0-3).
    - **Thalassemia:** 0=Normal, 1=Fixed Defect, 2=Reversible Defect.
    """)

if st.button('Predict Heart Disease Risk'):
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
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        if prediction[0] == 0:
            st.success('🎉 The person is unlikely to have Heart Disease.')
        else:
            st.error('⚠️ The person may have Heart Disease. Please consult a doctor.')
        st.markdown('</div>', unsafe_allow_html=True)

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