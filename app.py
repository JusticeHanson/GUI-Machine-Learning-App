# Import necessary libraries
import streamlit as st

# Configure the page
st.set_page_config(
    page_title='Home Page',
    page_icon='👨‍💻',
    layout='wide',
    initial_sidebar_state='auto'
)

# Add custom CSS to adjust the width of the sidebar
st.markdown("""
    <style> 
        section[data-testid="stSidebar"] {
            width: 200px !important;
        }
    </style> 
""", unsafe_allow_html=True)

def main():
    # Placeholder for authentication check
    # You can replace this with your actual authentication logic
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = False
    if 'name' not in st.session_state:
        st.session_state['name'] = 'Guest'

    if st.session_state['authentication_status']:
        st.write(f'Welcome *{st.session_state["name"]}*')
        st.header('Customer Churn Prediction App.')

        cols = st.columns(2)

        # Churn Prediction Status
        with cols[0]:
            st.subheader('Churn Prediction Status')
            st.write("This application provides a platform for predicting the churn status of customers by leveraging historical data encompassing customer demographics, subscription details, account information, and their corresponding churn status.")

        # Application Features
        with cols[0]:
            st.subheader('Application Features')
            st.markdown("""                
                * Data View - View proprietary data
                * Dashboard - Shows EDA and KPIs with other analytical questions
                * Predict - Allows user to predict churn status from two available models
                * History - Displays all previous predictions made using the app
            """)

        # Key Advantages
        with cols[0]:
            st.subheader('Key Advantages')
            st.markdown("""
                Discover the advantages of using this Churn Prediction App, such as:
                * Accurate predictions
                * User-friendly interface
            """)

        # How to run the app
        with cols[1]:
            st.subheader('How to Run the App')
            st.write("Follow the steps to run the Customer Churn Prediction App and make accurate predictions for customer churn.")
            st.code("""
                # Activate virtual environment
                venv/Scripts/activate

                # Run the Streamlit app
                streamlit run app.py
            """, language="python")

        # Machine Learning Integration
        with cols[1]:
            st.subheader('Machine Learning Integration')
            st.write("Learn about the machine learning models integrated into the app, including Gradient Boosting and Support Vector models.")

        # Need Assistance
        with cols[1]:
            st.subheader('Need Assistance?')
            st.write("If you need any assistance or have questions, feel free to reach out. Email: just.hanson1@gmail.com")
            cols = st.columns(4)
            with cols[0]:
                st.button("GitHub", url="https://github.com/JusticeHanson/GUI-Machine-Learning-App.git")
            with cols[1]:
                st.button("LinkedIn", url="http://www.linkedin.com/in/justice-hanson")

    else:
        st.write("You need to log in to access this page.")
        st.write("Please contact support for login details.")

if __name__ == '__main__':
    main()
