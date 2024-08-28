import streamlit as st
import plotly.express as px
import pandas as pd
import streamlit_shadcn_ui as ui

# Configure the page
st.set_page_config(
    page_title='Dashboard',
    page_icon='📊',
    layout='wide'
)

# --------- Add custom CSS to adjust the width of the sidebar
st.markdown("""
    <style> 
    section[data-testid="stSidebar"] {
        width: 200px !important;
    }
    </style> 
    """, unsafe_allow_html=True,
)

def dashboard_page():
    # Set header for page
    st.title('Dashboard')

    # ------ Set visualization view page
    col1, col2, col3 = st.columns(3)
    with col2:
        options = st.selectbox('Choose viz to display', options=['', 'EDA Dashboard', 'KPIs Dashboard'])

    # ------ Load Dataset from remote location
    @st.cache_data(show_spinner='Loading data')
    def load_data():
        df = pd.read_csv('./data/cleaned_merged.csv')
        return df

    df = load_data()

    def eda_viz():
        st.subheader('EDA Dashboard')
        column1, column2 = st.columns(2)
        with column1:
            fig = px.histogram(df, x='tenure', title='Distribution of Tenure')
            st.plotly_chart(fig)
        with column1:
            fig = px.histogram(df, x='MonthlyCharges', title='Distribution of MonthlyCharges')
            st.plotly_chart(fig)
        with column1:
            fig = px.histogram(df, x='TotalCharges', title='Distribution of TotalCharges')
            st.plotly_chart(fig)

        with column2:
            fig = px.bar(df, x='Churn', title='Churn Distribution')
            st.plotly_chart(fig)
        with column2:
            fig = px.box(df, x='gender', y='TotalCharges', title='Total Charges Distribution across Gender')
            st.plotly_chart(fig)

    def kpi_viz():
        st.subheader('KPIs Dashboard')
        st.markdown('---')
        cols = st.columns(6)
        st.markdown('---')

        # ------- Grand Total Charges
        with cols[0]:
            grand_tc = df['TotalCharges'].sum()
            ui.metric_card(title="Grand TotalCharges", content=f"{'{:,.2f}'.format(grand_tc)}", key="card1")

        # ------- Grand Monthly Charges
        with cols[1]:
            grand_mc = df['MonthlyCharges'].sum()        
            ui.metric_card(title="Grand MonthlyCharges", content=f"{'{:,.2f}'.format(grand_mc)}", key="card2")

        # ------- Average Customer Tenure
        with cols[2]:
            average_tenure = df['tenure'].mean()        
            ui.metric_card(title="Average Tenure", content=f"{'{:,.2f}'.format(average_tenure)}", key="card3")

        # ------- Churned Customers
        with cols[3]:
            churned = len(df.loc[df['Churn'] == 1])
            ui.metric_card(title="Churned Customers", content=f"{churned}", key="card4")
        
        # ------ Total Customers
        with cols[4]:
            total_customers = df.shape[0]
            ui.metric_card(title="Total Customers", content=f"{total_customers}", key="card5")
        
        # ------ Percentage of Customers with Dependents
        with cols[5]:
            pct_dependents = df['Dependents'].mean() * 100
            ui.metric_card(title="Customers with Dependents (%)", content=f"{'{:.2f}'.format(pct_dependents)}%", key="card6")

        st.markdown('---')
        cols2 = st.columns(6)
        st.markdown('---')

        # ------- Average Monthly Charges per Customer
        with cols2[0]:
            avg_mc_per_customer = df['MonthlyCharges'].mean()
            ui.metric_card(title="Avg MonthlyCharges per Customer", content=f"{'{:,.2f}'.format(avg_mc_per_customer)}", key="card7")

        # ------- Churn Rate
        with cols2[1]:
            churn_rate = (df['Churn'].mean()) * 100
            ui.metric_card(title="Churn Rate (%)", content=f"{'{:.2f}'.format(churn_rate)}%", key="card8")

        # ------- Total Dependents
        with cols2[2]:
            total_dependents = df['Dependents'].sum()
            ui.metric_card(title="Total Dependents", content=f"{total_dependents}", key="card9")
        
        # ------- Percentage of Customers with Multiple Lines
        with cols2[3]:
            pct_multiple_lines = df['MultipleLines'].apply(lambda x: 1 if x == 'Yes' else 0).mean() * 100
            ui.metric_card(title="Customers with Multiple Lines (%)", content=f"{'{:.2f}'.format(pct_multiple_lines)}%", key="card10")
        
        # ------- Average Total Charges
        with cols2[4]:
            avg_total_charges = df['TotalCharges'].mean()
            ui.metric_card(title="Average TotalCharges", content=f"{'{:,.2f}'.format(avg_total_charges)}", key="card11")

        # ------- Gender Distribution
        with cols2[5]:
            male_customers = df[df['gender'] == 'Male'].shape[0]
            female_customers = df[df['gender'] == 'Female'].shape[0]
            gender_distribution = f"Male: {male_customers}, Female: {female_customers}"
            ui.metric_card(title="Gender Distribution", content=gender_distribution, key="card12")

    def analytical_ques_viz():
        if df.empty:
            st.warning("Data not available for Analytical Questions")
            return

        # ------ Answer Analytical Question 1
        if 'gender' in df.columns and 'Dependents' in df.columns and 'Churn' in df.columns:
            mal_churned_customers = df[(df['gender']=='Male') & (df['Dependents']== 1) & (df['Churn']== 1)]['PaymentMethod'].value_counts()
            values = mal_churned_customers.values
            labels = mal_churned_customers.index
            treemap_df = pd.DataFrame({'labels': labels, 'values': values})
            fig = px.treemap(treemap_df, path=['labels'], values='values', color='values',
                            color_continuous_scale='Blues', title='Q1. How many male customers with dependents churned given their payment method?')
            st.plotly_chart(fig)
        else:
            st.warning("One or more required columns are missing for Analytical Question 1")

        # ------ Answer Analytical Question 2
        if 'gender' in df.columns and 'Dependents' in df.columns and 'Churn' in df.columns:
            fem_churned_customers = df[(df['gender']=='Female') & (df['Dependents']== 1) & (df['Churn']== 1)]['PaymentMethod'].value_counts()
            values = fem_churned_customers.values
            labels = fem_churned_customers.index
            treemap_df = pd.DataFrame({'labels': labels, 'values': values})
            fig = px.treemap(treemap_df, path=['labels'], values='values', color='values',
                            color_continuous_scale='Blues', title='Q2. How many female customers with dependents churned given their payment method?')
            st.plotly_chart(fig)
        else:
            st.warning("One or more required columns are missing for Analytical Question 2")

        # ------ Answer Analytical Question 3
        if 'MultipleLines' in df.columns and 'gender' in df.columns and 'Churn' in df.columns:
            churned = df[df['Churn'] == 1]
            fig = px.bar(churned, x='MultipleLines', color='gender', barmode='group',
                        title='Q3. What is the distribution for the customers who churned given their multiple lines status?',
                        labels={'MultipleLines': 'Multiple Lines', 'gender': 'Gender'})
            st.plotly_chart(fig)
        else:
            st.warning("One or more required columns are missing for Analytical Question 3")

        # ------ Answer Analytical Question 4
        if 'gender' in df.columns and 'MonthlyCharges' in df.columns:
            monthly_charges = df.groupby('gender')['MonthlyCharges'].sum().reset_index()
            fig = px.pie(monthly_charges, names='gender', values='MonthlyCharges',
                        title='Q4. What percentage of MonthlyCharges was accumulated given the customer gender?',
                        color='gender',
                        labels={'gender': 'Gender', 'MonthlyCharges': 'Monthly Charges'})
            st.plotly_chart(fig)
        else:
            st.warning("One or more required columns are missing for Analytical Question 4")

        # ------ Answer Analytical Question 5
        if 'Churn' in df.columns and 'TotalCharges' in df.columns:
            monthly_charges = df.groupby('Churn')['TotalCharges'].sum().reset_index()
            fig = px.pie(monthly_charges, names='Churn', values='TotalCharges',
                        title='Q5. What percentage of TotalCharges was accumulated given customer churn status?',
                        color='Churn',
                        labels={'Churn': 'Churn', 'TotalCharges': 'Total Charges'})
            st.plotly_chart(fig)
        else:
            st.warning("One or more required columns are missing for Analytical Question 5")

    # Main Logic
    if options == 'EDA Dashboard':
        eda_viz()
    elif options == 'KPIs Dashboard':
        kpi_viz()
    else:
        analytical_ques_viz()

if __name__ == "__main__":
    dashboard_page()
