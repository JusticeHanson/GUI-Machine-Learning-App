import streamlit as st
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from io import BytesIO
import joblib
import os

# Configure the page
st.set_page_config(
    page_title='Predictions',
    page_icon='🔮',
    layout='wide'
)

# --------- Add custom CSS to adjust the width of the sidebar
st.markdown(""" 
    <style> 
        section[data-testid="stSidebar"] { width: 200px !important; }
    </style> """, unsafe_allow_html=True)

st.title("Predict Customer Churn!")

column1, column2 = st.columns([.6, .4])
with column1:
    model_option = st.selectbox('Choose which model to use for prediction', options=['Gradient Boosting', 'Support Vector'])

# Define file paths
local_model1_path = 'model/GradientBoosting.joblib'
local_model2_path = 'model/SupportVector.joblib'
local_encoder_path = 'model/label_encoder.joblib'

# -------- Function to load the model from local files
@st.cache_resource(show_spinner="Loading model")
def gb_pipeline():
    model = joblib.load(local_model1_path)
    return model

@st.cache_resource(show_spinner="Loading model")
def sv_pipeline():
    model = joblib.load(local_model2_path)
    return model

# --------- Function to load encoder from local files
def load_encoder():
    encoder = joblib.load(local_encoder_path)
    return encoder

# --------- Create a function for model selection
def select_model():
    if model_option == 'Gradient Boosting':
        model = gb_pipeline()
    else:  # Ensure 'Support Vector' is handled correctly
        model = sv_pipeline()
    encoder = load_encoder()
    return model, encoder

# Custom function to deal with cleaning the total charges column
class TotalCharges_cleaner(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        # Replace empty string with NA
        X['TotalCharges'].replace(' ', np.nan, inplace=True)
        # Convert the values in the TotalCharges column to a float
        X['TotalCharges'] = X['TotalCharges'].astype(float)
        return X
        
    def __getstate__(self):
        return {}

    def __setstate__(self, state):
        pass
        
    def get_feature_names_out(self, input_features=None):
        return input_features

# Create a class to deal with dropping Customer ID from the dataset
class columnDropper(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        return X.drop('customerID', axis=1)
        
    def get_feature_names_out(self, input_features=None):
        if input_features is None:
            return None
        return [feature for feature in input_features if feature != 'customerID']

# Initialize prediction in session state
if 'prediction' not in st.session_state:
    st.session_state['prediction'] = None
if 'prediction_proba' not in st.session_state:
    st.session_state['prediction_proba'] = None

# ------- Create a function to make prediction
def make_prediction(model, encoder):
    customerID = st.session_state['customer_id']
    gender = st.session_state['gender']
    SeniorCitizen = st.session_state['senior_citizen']
    Partner = st.session_state['partners']
    Dependents = st.session_state['dependents']
    tenure = st.session_state['tenure']
    PhoneService = st.session_state['phone_service']
    MultipleLines = st.session_state['multiple_lines']
    InternetService = st.session_state['internet_service']
    OnlineSecurity = st.session_state['online_security']
    OnlineBackup = st.session_state['online_backup']
    DeviceProtection = st.session_state['device_protection']
    TechSupport = st.session_state['tech_support']
    StreamingTV = st.session_state['streaming_tv']
    StreamingMovies = st.session_state['streaming_movies']
    Contract = st.session_state['contract']
    PaperlessBilling = st.session_state['paperless_billing']
    PaymentMethod = st.session_state['payment_method']
    MonthlyCharges = st.session_state['monthly_charges']
    TotalCharges = st.session_state['total_charges']
        
    columns = ['customerID', 'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
                'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
                'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
                'Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges']
        
    values = [[customerID, gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService,
            MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection,
            TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling,
            PaymentMethod, MonthlyCharges, TotalCharges]]
        
    data = pd.DataFrame(values, columns=columns)

    # Get the value for prediction
    prediction = model.predict(data)
    prediction = encoder.inverse_transform(prediction)
    st.session_state['prediction'] = prediction

    # Get the value for prediction probability
    prediction_proba = model.predict_proba(data)
    st.session_state['prediction_proba'] = prediction_proba

    data['Churn'] = prediction
    data['Model'] = model_option

    if not os.path.exists('./data'):
        os.makedirs('./data')
        
    data.to_csv('./data/history.csv', mode='a', header=not os.path.exists('./data/history.csv'), index=False)

    return prediction, prediction_proba

# ------- Prediction page creation
def input_features():
    with st.form('features'):
        model_pipeline, encoder = select_model()
        col1, col2 = st.columns(2)

        # ------ Collect customer information
        with col1:
            st.subheader('Demographics')
            customer_id = st.text_input('Customer ID', value="", placeholder='eg. 1234-ABCDE')
            gender = st.radio('Gender', options=['Male', 'Female'], horizontal=True)
            partners = st.radio('Partners', options=['Yes', 'No'], horizontal=True)
            dependents = st.radio('Dependents', options=['Yes', 'No'], horizontal=True)
            senior_citizen = st.radio("Senior Citizen ('Yes-1, No-0')", options=[1, 0], horizontal=True)
            
        # ------ Collect customer account information
        with col1:
            st.subheader('Customer Account Info.')
            tenure = st.number_input('Tenure', min_value=0, max_value=70)
            contract = st.selectbox('Contract', options=['Month-to-month', 'One year', 'Two year'])
            payment_method = st.selectbox('Payment Method',
                                          options=['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'])
            paperless_billing = st.radio('Paperless Billing', ['Yes', 'No'], horizontal=True)
            monthly_charges = st.number_input('Monthly Charges', placeholder='Enter amount...')
            total_charges = st.number_input('Total Charges', placeholder='Enter amount...')
            
        # ------ Collect customer subscription information
        with col2:
            st.subheader('Subscriptions')
            phone_service = st.radio('Phone Service', ['Yes', 'No'], horizontal=True)
            multiple_lines = st.selectbox('Multiple Lines', ['Yes', 'No', 'No internet service'])
            internet_service = st.selectbox('Internet Service', ['DSL', 'Fiber optic', 'No'])
            online_security = st.selectbox('Online Security', ['Yes', 'No', 'No internet service'])
            online_backup = st.selectbox('Online Backup', ['Yes', 'No', 'No internet service'])
            device_protection = st.selectbox('Device Protection', ['Yes', 'No', 'No internet service'])
            tech_support = st.selectbox('Tech Support', ['Yes', 'No', 'No internet service'])
            streaming_tv = st.selectbox('Streaming TV', ['Yes', 'No', 'No internet service'])
            streaming_movies = st.selectbox('Streaming Movies', ['Yes', 'No', 'No internet service'])

        # Add the submit button
        submitted = st.form_submit_button('Predict')
        if submitted:
            st.session_state['customer_id'] = customer_id
            st.session_state['gender'] = gender
            st.session_state['senior_citizen'] = senior_citizen
            st.session_state['partners'] = partners
            st.session_state['dependents'] = dependents
            st.session_state['tenure'] = tenure
            st.session_state['phone_service'] = phone_service
            st.session_state['multiple_lines'] = multiple_lines
            st.session_state['internet_service'] = internet_service
            st.session_state['online_security'] = online_security
            st.session_state['online_backup'] = online_backup
            st.session_state['device_protection'] = device_protection
            st.session_state['tech_support'] = tech_support
            st.session_state['streaming_tv'] = streaming_tv
            st.session_state['streaming_movies'] = streaming_movies
            st.session_state['contract'] = contract
            st.session_state['paperless_billing'] = paperless_billing
            st.session_state['payment_method'] = payment_method
            st.session_state['monthly_charges'] = monthly_charges
            st.session_state['total_charges'] = total_charges
            
            # Make the prediction
            make_prediction(model_pipeline, encoder)

    return True

if __name__ == '__main__':
    input_features()
    
    prediction = st.session_state['prediction']
    probability = st.session_state['prediction_proba']    

    if prediction is None:
        cols = st.columns([3, 4, 3])
        with cols[1]:
            st.markdown('#### Predictions will show here ⤵️')
        cols = st.columns([.25, .5, .25])
        with cols[1]:
            st.markdown('##### No predictions made yet. Make a prediction.')
    else:
        if prediction == "Yes":
            cols = st.columns([.1, .8, .1])
            with cols[1]:
                st.markdown(f'### The customer will churn with a {round(probability[0][1], 2)} probability.')
            cols = st.columns([.3, .4, .3])
            with cols[1]:
                st.success('Churn status predicted successfully🎉')
        else:
            cols = st.columns([.1, .8, .1])
            with cols[1]:
                st.markdown(f'### The customer will not churn with a {round(probability[0][0], 2)} probability.')
            cols = st.columns([.3, .4, .3])
            with cols[1]:
                st.success('Churn status predicted successfully🎉')