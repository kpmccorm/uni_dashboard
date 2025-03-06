import streamlit as st
import plotly.express as px

st.title('University Admissions Tracking')
uni_data = pd.read_csv('/content/university_student_dashboard_data.csv')

fig = px.bar(uni_data,x='Year',y='Enrolled',title="Enrollment by Academic Year")

st.plotly_chart(fig)
