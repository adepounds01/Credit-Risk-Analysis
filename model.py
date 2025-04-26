import streamlit as st
import joblib
import pandas as pd

# Load the saved pipeline (ensure that this pipeline was built using your dataset columns)
pipeline = joblib.load('pipeline.joblib')

def make_prediction(person_age, person_income, person_emp_length, loan_amnt, loan_int_rate, 
                    loan_percent_income, cb_person_cred_hist_length,
                    person_home_ownership, loan_intent, loan_grade, cb_person_default_on_file):
    """
    Given applicant details, this function uses the pre-trained pipeline to predict 
    the probability of loan approval and classify the risk.
    """
    # Create a dictionary with the input data
    model_data = {
        'person_age': person_age,
        'person_income': person_income,
        'person_emp_length': person_emp_length,
        'loan_amnt': loan_amnt,
        'loan_int_rate': loan_int_rate,
        'loan_percent_income': loan_percent_income,
        'cb_person_cred_hist_length': cb_person_cred_hist_length,
        'person_home_ownership': person_home_ownership,
        'loan_intent': loan_intent,
        'loan_grade': loan_grade,
        'cb_person_default_on_file': cb_person_default_on_file
    }
    
    # Convert input data to DataFrame (ensure columns match training data)
    input_df = pd.DataFrame([model_data])
    
    # Make prediction: assuming positive class (index 1) corresponds to loan approval.
    approval_probability = pipeline.predict_proba(input_df)[:, 1][0]
    probability_percentage = approval_probability * 100

    # Risk classification thresholds (adjust as needed)
    if approval_probability >= 0.70:
        risk_level = "Low Risk"
        suggestion = "Proceed with the application."
    elif approval_probability >= 0.40:
        risk_level = "Moderate Risk"
        suggestion = "A further review is recommended before proceeding."
    else:
        risk_level = "High Risk"
        suggestion = "Consider rejecting the application or request additional information."

    # Return a comprehensive message
    return (f"Predicted Loan Approval Probability: {probability_percentage:.1f}%\n\n"
            f"Risk Level: {risk_level}\n\n"
            f"Recommendation: {suggestion}")

# Streamlit app layout for loan approval prediction
def app():
    st.title('Loan Approval & Risk Predictor')
    st.write('Enter the applicant details below to predict the likelihood of loan approval, '
             'classify the risk level, and get a suggested action.')
    
    with st.form("loan_details_form"):
        st.header("Applicant Details")
        
        # Numeric inputs
        person_age = st.slider('Person Age', 18, 100, 35)
        person_income = st.number_input('Person Income', min_value=0, value=50000)
        person_emp_length = st.slider('Employment Length (years)', 0.0, 40.0, 10.0, step=0.5)
        loan_amnt = st.number_input('Loan Amount', min_value=0, value=15000)
        loan_int_rate = st.slider('Loan Interest Rate (%)', 0.0, 30.0, 12.5, step=0.1)
        loan_percent_income = st.slider('Loan Percent Income', 0.0, 100.0, 30.0, step=0.1)
        cb_person_cred_hist_length = st.slider('Credit History Length (years)', 0, 50, 5)
        
        # Categorical inputs
        person_home_ownership = st.selectbox('Person Home Ownership', 
                                               options=["RENT", "OWN", "MORTGAGE", "OTHER"])
        loan_intent = st.selectbox('Loan Intent', 
                                   options=["credit_card", "debt_consolidation", "home_improvement", 
                                            "small_business", "major_purchase", "medical", "moving", 
                                            "vacation", "wedding"])
        loan_grade = st.selectbox('Loan Grade', options=["A", "B", "C", "D", "E", "F", "G"])
        cb_person_default_on_file = st.selectbox('Credit Default on File', options=["N", "Y"])
        
        # Form submission button
        submit_button = st.form_submit_button("Predict")
        
    if submit_button:
        prediction_result = make_prediction(
            person_age, person_income, person_emp_length, loan_amnt, loan_int_rate, 
            loan_percent_income, cb_person_cred_hist_length,
            person_home_ownership, loan_intent, loan_grade, cb_person_default_on_file
        )
        st.success(prediction_result)

if __name__ == '__main__':
    app()
