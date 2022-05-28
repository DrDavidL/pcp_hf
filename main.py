import streamlit as st
import numpy as np
from numpy import log as ln, mean

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


coeff = {1: (41.94101, 20.54973, 2.88334, 51.75667), 2: (-0.88115, 0, 0, 0), 3: (1.030508, 12.94937, 2.31106, 28.97791), 4: (0, -2.96923, 0, -6.59777),
 5: (0.91252, 11.86273,  2.17229, 28.1853), 6: (0, -2.72538, 0, -6.42425), 7: (0.73839, 11.01752, 1.65337, 0.76532),  8: (0, -2.50777, -0.24665, 0),
 9: (0.90072, 1.04503, 0.64704, 0.96695), 10: (0.77805, 0.91807, 0.57891, 0.79561), 11: (0.49323, 0, 0, 0.32646), 12: (-0.43683, -0.07455, -0.80691, 0),
 13: (37.21577, 1.32948, 1.16289, 21.24763), 14: (-8.83278, 0, 0, -5.00068), 15: (0.63224, 1.06089, 0.72646, 1.27475)}


if ishtn:
    features[5] = 0
    features[6] = 0
else:
    features[3] = 0
    features[4] = 0

if isdiabetes:
    features[10] = 0
else:
    features[9] = 0

if sex == 'male' and race == 'white':
    flex = 0
elif sex == 'female' and race == 'white':
    flex = 1
elif sex == 'male' and race == 'black':
    flex = 2
else:
    flex = 3

sex_race_coeff = {}

templist = []
for key in coeff:
    templist = list(coeff[key])
    sex_race_coeff[key] = templist[flex]

coefxvalue = {}
for key in features:
    coefxvalue[key] = features[key] * sex_race_coeff[key]






sum_coefxvalue = sum(coefxvalue.values())

mean_coefxvalue= sum_coefxvalue / 15


st.write('sum of coefxvalue', sum_coefxvalue)
st.write('mean of coefxvalue', mean_coefxvalue)

survival = (0.98752, 0.99348, 0.98295, 0.9926 )

risk = 1 -  survival[flex]**(sum_coefxvalue - mean_coefxvalue)

riskpct = risk * 100

st.write('The 10 year risk for heart failure is: ', round(riskpct, 2), "%.")
