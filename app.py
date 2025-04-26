# app.py
import streamlit as st  # MUST BE FIRST IMPORT

# Set page config IMMEDIATELY after Streamlit import
st.set_page_config(
    page_title="Credit Risk Radar",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Now import other dependencies
import pandas as pd
from pathlib import Path
from PIL import Image
from streamlit_option_menu import option_menu
import Dashboard, Contact
from Prediction import app as prediction_app 

# ----------------------- Rest of app.py -----------------------
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
logo_path = current_dir / "Photos" / "logo.png"
logo = Image.open(logo_path)

# Import dataset
df = pd.read_csv('preprocessed_data.csv')

# Style configuration
style = {
    "nav-link": {"font-family": "Monospace, Arial", "--hover-color": "SkyBlue"},
    "nav-link-selected": {"background-color": "rgb(10, 0, 124)", "font-family": "Monospace, Arial"},
}

class MultiPage:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({"title": title, "function": function})

    def run(self):
        with st.sidebar:
            st.title('Credit Risk Radar')
            st.image(logo, width=175)
            app = option_menu(
                None,
                options=['Dashboard', 'Check the Risk', 'Contact'],
                icons=["pie-chart-fill", "person-check-fill", "file-person-fill"],
                styles=style,
                default_index=0,
            )

        if app == 'Dashboard':
            Dashboard.app(df)
        elif app == 'Check the Risk':
            prediction_app()
        elif app == 'Contact':
            Contact.app(st, current_dir, Image)

if __name__ == "__main__":
    MultiPage().run()