import streamlit as st
import numpy as np
from numpy import log as ln, mean

st.title("PCP HF Risk Calculator")
st.write('*10-Year Heart Failure Risk Calculator from Pooled Cohort Analysis (PCP-HF)*')

col1, col2, col3 = st.columns([2,1,4])

with col1:

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
                7: (issmoker + 0), 8: (issmoker +0)*ln(age), 9: ln(glucose), 10: ln(glucose), 11: ln(tchol),
                12: ln(hdl), 13: ln(bmi), 14: ln(age)*ln(bmi), 15: ln(qrs) }


    coeff = {1: (41.94101, 20.54973, 2.88334, 51.75667), 2: (-0.88115, 0, 0, 0), 3: (1.030508, 12.94937, 2.31106, 28.97791), 4: (0, -2.96923, 0, -6.59777),
    5: (0.91252, 11.86273,  2.17229, 28.1853), 6: (0, -2.72538, 0, -6.42425), 7: (0.73839, 11.01752, 1.65337, 0.76532),  8: (0, -2.50777, -0.24665, 0),
    9: (0.90072, 1.04503, 0.64704, 0.96695), 10: (0.77805, 0.91807, 0.57891, 0.79561), 11: (0.49323, 0, 0, 0.32646), 12: (-0.43683, -0.07455, -0.80691, 0),
    13: (37.21577, 1.32948, 1.16289, 21.24763), 14: (-8.83278, 0, 0, -5.00068), 15: (0.63224, 1.06089, 0.72646, 1.27475)}

    # Set measured values to zero if not applicable, e.g., whether treated HTN or diabetes are present. 
    # Set new dm or HTN specific features (cond_features) as same as (features) except for HTN or DM values

    cond_features = features

    if ishtn:
        cond_features[5] = 0
        cond_features[6] = 0
    else:
        cond_features[3] = 0
        cond_features[4] = 0

    if isdiabetes:
        cond_features[10] = 0
    else:
        cond_features[9] = 0

    # Set the index ("flex" below) for the corresponding sex and race in all lists: WM, WF, BM, BF. 

    survival = (0.98752, 0.99348, 0.98295, 0.9926 )

    if sex == 'male' and race == 'white':
        flex = 0
    elif sex == 'female' and race == 'white':
        flex = 1
    elif sex == 'male' and race == 'black':
        flex = 2
    else:
        flex = 3

    # Filter the dictionary of coefficients according to sex and race for the current input.

    sex_race_coeff = {}

    templist = []
    for key in coeff:
        templist = coeff[key]
        sex_race_coeff[key] = templist[flex]

    # Make a key value pair for coefficients x values. 

    coefxvalue = {}
    for key in cond_features:
        coefxvalue[key] = cond_features[key] * sex_race_coeff[key]

    sum_coefxvalue = sum(coefxvalue.values())

    mean_coef = sum(sex_race_coeff.values())/15

    mean_coefxvalue = {}
    for key in cond_features:
        mean_coefxvalue[key] = cond_features[key] * mean_coef

    mean_cv = sum(mean_coefxvalue.values())

        # Below used for troubleshooting

    # st.write('Condition specific features', cond_features )

    # st.write('Sex and race specific coefficients', sex_race_coeff )

    MeanCV = [171.59, 99.7321, 28.7369, 233.978]

    # Below used for troubleshooting

    # st.write('sum of coefxvalue', sum_coefxvalue)
    # st.write('mean of coefxvalue', MeanCV[flex])

    s0 = survival[flex]

    IndX = sum_coefxvalue



    risk = 1 -  s0**2.718281828459**(sum_coefxvalue - MeanCV[flex])

    riskpct = risk * 100


with col2:

    st.write(' ')

with col3:


    st.markdown('## *The 10 year risk of heart failure for a patient with the parameters selected:*')
    st.title(str(round(riskpct,2)) + ' %')

    

    st.markdown('### Summary of inputs:')

    st.write('Age is: ' + str(age))
    race
    sex
    if isdiabetes:
        st.write("With diabetes")
    else:
        st.write("Without diabetes")

    if ishtn:
        st.write("With treated HTN")
    else:
        st.write("Without treated HTN")
    
    st.write('BMI is: ' + str(round(bmi,1)))

    if issmoker:
        st.write('Is a smoker')
    else:
        st.write('Is a non-smoker')
    
    st.write('SBP: ' + str(sbp) + ' mmHg')
    st.write('Total cholesterol: ' + str(tchol) + ' mg/dL')
    st.write('HDL: ' + str(hdl) + ' mg/dL')
    st.write('QRS interval: ' + str(qrs) +' msec')

    st.markdown('### Equation Details:')

    
    st.latex("Risk = 1 - S_{0}^{e^{(IndX - MeanCV)}}")

    st.latex("S_{0} = survival\;(baseline)") 

    st.latex("IndX = sum\;of\;(coefficient\;x\;value)") 

    st.latex("MeanCV = Sex\;and\;gender \;specific \;mean \;coefficient \;x \;value") 

    st.markdown('*Reference*:')

    st.markdown('Khan S, Ning H, Shah S, et al. 10-Year Risk Equations for Incident Heart Failure in the General Population. J Am Coll Cardiol. 2019 May, 73 (19) 2388-2397. https://doi.org/10.1016/j.jacc.2019.02.057')

    st.markdown('Github URL: https://github.com/DrDavidL/pcp_hf')
  



    
  


