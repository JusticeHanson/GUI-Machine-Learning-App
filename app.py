# Import necessary libraries
import streamlit as st

# Configure the page
st.set_page_config(
    page_title='Customer Churn Prediction App',
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
    st.header('Customer Churn Prediction App')

    st.write(
        """
        Welcome to the **Customer Churn Prediction App**! Our app is designed to help businesses understand and predict customer churn using advanced data analysis and machine learning techniques.
        """
    )

    cols = st.columns(2)

    # Churn Prediction Status
    with cols[0]:
        st.subheader('About the App')
        st.write(
            """
            This application leverages historical data to predict the likelihood of customer churn. By analyzing customer demographics, subscription details, and account information, the app helps businesses:
            
            * Identify customers at risk of churning
            * Understand factors influencing churn
            * Implement strategies to retain valuable customers
            
            With a user-friendly interface and powerful predictive models, our app provides actionable insights to enhance customer retention strategies.
            """
        )

    # Application Features
    with cols[0]:
        st.subheader('Key Features')
        st.markdown("""
            * **Data View**: Explore and analyze customer data to gain insights into churn patterns.
            * **Dashboard**: Visualize key metrics and trends through interactive charts and graphs.
            * **Predict**: Use our predictive models to estimate the likelihood of customer churn based on various factors.
            * **History**: Review past predictions and track changes over time.
            """)

    # Key Advantages
    with cols[0]:
        st.subheader('Why Use This App?')
        st.markdown("""
            * **Accurate Predictions**: Benefit from state-of-the-art machine learning models for reliable churn forecasts.
            * **Intuitive Interface**: Navigate through a user-friendly interface designed for ease of use.
            * **Actionable Insights**: Gain insights into customer behavior and retention strategies.
            * **Continuous Improvement**: Regular updates and enhancements to keep up with the latest trends and technologies.
            """)

    # How to Run the App
    with cols[1]:
        st.subheader('How to Get Started')
        st.write("Follow these steps to run the Customer Churn Prediction App:")
        st.code("""
            # Activate your virtual environment
            venv/Scripts/activate

            # Run the Streamlit app
            streamlit run app.py
            """, language="python")

    # Machine Learning Integration
    with cols[1]:
        st.subheader('Machine Learning Models')
        st.write(
            """
            Our app integrates advanced machine learning models, including Gradient Boosting and Support Vector Machines (SVM). These models are trained on historical data to deliver accurate predictions and help businesses make informed decisions.
            """)

    # Need Assistance
    with cols[1]:
        st.subheader('Need Help?')
        st.write(
            """
            If you encounter any issues or have questions, please don't hesitate to reach out:
            - **Email**: just.hanson1@gmail.com
            - **GitHub**: [GitHub Repository](https://github.com/JusticeHanson/GUI-Machine-Learning-App.git)
            - **LinkedIn**: [Connect on LinkedIn](http://www.linkedin.com/in/justice-hanson)
            """)

if __name__ == '__main__':
    main()
