import streamlit as st
import joblib
import pandas as pd
from pathlib import Path

@st.cache_resource
def load_pipeline():
    """Load and cache the prediction pipeline."""
    try:
        return joblib.load(Path('pipeline.joblib'))
    except FileNotFoundError:
        st.error("❌ Model pipeline not found. Ensure 'pipeline.joblib' exists.")
        st.stop()

def create_input_form():
    """Creates an organized form for user input."""
    with st.form("loan_app_form"):
        # Applicant Demographics
        with st.expander("📄 Applicant Demographics", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                age = st.slider("Age", 18, 100, 30)
                income = st.number_input("Annual Income ($)", 0, 1_000_000, 60000, step=1000)
            with col2:
                emp_length = st.slider("Employment History (years)", 0.0, 40.0, 5.0, 0.5)
                credit_history = st.slider("Credit History Length (years)", 0, 50, 7)

        # Loan Details
        with st.expander("💵 Loan Details", expanded=True):
            col3, col4 = st.columns(2)
            with col3:
                loan_amt = st.number_input("Loan Amount ($)", 0, 500_000, 25000, step=500)
                int_rate = st.slider("Interest Rate (%)", 0.0, 30.0, 8.5, 0.1)
            with col4:
                loan_income_ratio = st.slider("Debt-to-Income Ratio (%)", 0.0, 100.0, 35.0, 0.1)
                loan_grade = st.selectbox("Credit Grade", ["A", "B", "C", "D", "E", "F", "G"])

        # Financial History
        with st.expander("🏦 Financial History", expanded=False):
            col5, col6 = st.columns(2)
            with col5:
                home_status = st.selectbox("Housing Status", ["RENT", "OWN", "MORTGAGE", "OTHER"])
                loan_purpose = st.selectbox("Loan Purpose", [
                    "Debt Consolidation", "Home Improvement", "Business Investment",
                    "Medical Expenses", "Education", "Major Purchase", "Other"
                ])
            with col6:
                default_history = st.radio("Default History", ["No", "Yes"], horizontal=True)

        submitted = st.form_submit_button("🚀 Analyze Application")
        
        # Return a dictionary with field names matching those used during training.
        return submitted, {
            'person_age': age,
            'person_income': income,
            'person_emp_length': emp_length,
            'loan_amnt': loan_amt,
            'loan_int_rate': int_rate,
            'loan_percent_income': loan_income_ratio,
            'cb_person_cred_hist_length': credit_history,
            'person_home_ownership': home_status,
            'loan_intent': loan_purpose.upper().replace(" ", "_"),
            'loan_grade': loan_grade,
            'cb_person_default_on_file': "Y" if default_history == "Yes" else "N"
        }

def display_results(probability):
    """Displays risk assessment results and detailed analysis."""
    risk_color = {
        "High Risk": "#FF4B4B",
        "Moderate Risk": "#FFC300",
        "Low Risk": "#00D474"
    }
    
    prob_percent = probability * 100
    risk = "Low Risk" if prob_percent >= 70 else "Moderate Risk" if prob_percent >= 40 else "High Risk"

    with st.container():
        st.subheader("Risk Assessment Summary")
        
        col_a, col_b = st.columns([1, 3])
        with col_a:
            st.metric(label="Approval Probability", value=f"{prob_percent:.1f}%")
        with col_b:
            st.progress(probability, text=f"{risk} Classification")
        
        with st.expander("📊 Analysis Details"):
            st.markdown(f"""
            **Risk Category:**  
            :{risk_color[risk].lower()}[{risk}]  
            
            **Recommendation:**  
            {"✅ Recommend approval" if risk == "Low Risk" else 
             "⚠️ Requires manual review" if risk == "Moderate Risk" else 
             "❌ Recommend decline"}
            
            **Key Factors:**  
            - Credit history score: {risk} impact  
            - Debt ratio: {('Within', 'Exceeding')[probability < 0.4]} guidelines  
            - Default history: {'No' if probability > 0.4 else 'Yes'} prior issues
            """)

def apply_custom_styles():
    """Inject custom CSS so that input boxes are black with white text."""
    st.markdown("""
    <style>
        /* Overall page background remains as default */
        
        /* Input containers: black background, white text */
        .stNumberInput, .stSlider, .stSelectbox, .stRadio {
            background-color: #000000;
            color: #ffffff;
            border-radius: 8px;
            padding: 12px;
        }
        
        /* Ensure labels inside input widgets are white */
        label, .stRadio > label, .stNumberInput > label, .stSlider > label, .stSelectbox > label {
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        
        /* Expander headers: black background, white text */
        .stExpanderHeader {
            background-color: #000000 !important;
            border-radius: 8px !important;
            padding: 12px !important;
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        
        /* Buttons: black background, white text */
        [data-testid="stFormSubmitButton"] button {
            background: #000000 !important;
            color: #ffffff !important;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        [data-testid="stFormSubmitButton"] button:hover {
            transform: scale(1.02);
            box-shadow: 0 4px 8px rgba(255,255,255,0.2);
        }
    </style>
    """, unsafe_allow_html=True)

# ----------------------- Main App Function -----------------------
def app():
    """Main prediction module for the Automated Loan Risk Analyzer."""
    apply_custom_styles()
    pipeline = load_pipeline()
    
    st.title("Automated Loan Risk Analyzer")
    st.caption("Advanced ML-powered credit assessment system")
    
    submitted, inputs = create_input_form()
    if submitted:
        with st.spinner("🔍 Analyzing financial patterns..."):
            try:
                proba = pipeline.predict_proba(pd.DataFrame([inputs]))[:, 1][0]
                display_results(proba)
            except Exception as e:
                st.error(f"⚠️ Analysis error: {str(e)}")
                st.info("Please validate all input fields and try again")

if __name__ == "__main__":
    app()
