import streamlit as st
import numpy as np
from numpy import log as ln

st.title("PCP HF Risk Calculator")
st.write('*10-Year Heart Failure Risk Calculator from Pooled Cohort Analysis (PCP-HF)*')
st.latex("Risk = 1 - S_{0}^{e^{(IndX - MeanCV)}}")


age = st.slider("Age:", min_value=30, max_value=80, value =50)



# weight = st.number_input('Enter weight in pounds', min_value=75.0, max_value=400.0, value = 160., step = 1.)

weight = st.slider("Weight (pounds)", min_value=75, max_value=400, value =150)

height = st.slider("Height (inches)", min_value=36, max_value=96, value =65)

bmi = 703 * weight / height**2

st.write('The BMI calculates to ', round(bmi,1))

ishtn = st.checkbox('HTN: Select if treated for hypertension.')

# if ishtn:
#      st.write('HTN is recorded!')


issmoker = st.checkbox('Smoking: Select if the patient smokes.')

# if issmoker:
#      st.write('Smoking is recorded!')

isdiabetes = st.checkbox('DM: Select if the patient has diabetes.')

# if isdiabetes:
#      st.write('Diabetes is recorded!')

sex = st.radio(
     "Please select a sex. (Note - limited to the options available in the published algorithm) ",
     ('female', 'male'))

race = st.radio(
    "Please select a race  (Note - limited to the options available in the published algorithm) ",
     ('black', 'white'))



sbp = st.slider("Current systolic blood pressure in mm Hg.", min_value=80, max_value=200, value =120)

glucose = st.slider("Fasting glucose mg/dL.", min_value=60, max_value=300, value =100)

tchol = st.slider("Total cholesterol in mg/dL.", min_value=80, max_value=300, value =160)

hdl = st.slider("HDL in mg/dL.", min_value=15, max_value=100, value =40)

qrs = st.slider("QRS duration in msec.", min_value=55, max_value=200, value =100)


features = {1: ln(age), 2: ln(age)**2, 3: ln(sbp), 4: ln(age)*ln(sbp), 5: ln(sbp), 6: ln(age)*ln(sbp), 
            7: issmoker + 0, 8: (issmoker +1)*ln(age), 9: ln(glucose), 10: ln(glucose), 11: ln(tchol),
            12: ln(hdl), 13: ln(bmi), 14: ln(age)*ln(bmi), 15: ln(qrs) }


wm_coeff = {1: 41.94101, 2: -0.88115, 3: 1.030508, 4: 0, 5: 0.91252, 6: 0, 7: 0.73839, 8: 0, 9: 0.90072, 
            10: 0.77805, 11: 0.49323, 12: -0.43683, 13: 37.21577, 14: -8.83278, 15: 0.63224}

tally = 0

for key in features:
    tally += features[key] * wm_coeff[key]

survival = 0.98752

risk = 1 -  survival**(tally -171.59)

riskpct = risk * 100

st.write('The 10 year risk for heart failure is ', round(riskpct, 2), "%")
