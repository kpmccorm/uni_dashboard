#libraries
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

#================================================================================
#app width
st.set_page_config(layout="wide")

#app title
st.title('University Admissions Tracking')

#initial data load
uni_data = pd.read_csv('university_student_dashboard_data.csv')

#================================================================================

#extra features
uni_data['Admissions Rate (%)'] = round((uni_data['Admitted']/uni_data['Applications'])*100,0).astype(int)
uni_data['Matriculation Rate (%)'] = round((uni_data['Enrolled']/uni_data['Admitted'])*100,0).astype(int)
uni_data = uni_data.sort_values(['Year','Term'],ascending=[True,True]) #Sort by year + term
uni_data['Semester'] =  uni_data['Year'].astype(str) + ' ' +uni_data['Term'] #Create a semester column and convert to ordered category

#define dataframe of metrics
metrics = uni_data[['Year','Term','Semester','Retention Rate (%)','Student Satisfaction (%)']].copy()
metrics = metrics.melt(id_vars=['Year','Term','Semester'],var_name='Metric',value_name='Value')
metrics['Metric'] = metrics['Metric'].str.replace(' (%)','')
metrics = metrics.groupby(['Year','Metric']).agg({'Value':'mean'}).reset_index()

#Define data for the departments
##Select columns
depts = ['Engineering', 'Business', 'Arts', 'Science']
uni_depts = uni_data[['Year','Term','Enrolled','Engineering Enrolled','Business Enrolled','Arts Enrolled','Science Enrolled']].copy()
uni_depts = uni_depts.rename(lambda x: x.replace(' Enrolled',''),axis=1)

##Calculate department enrollment shares
uni_depts['Engineering'] = round(uni_depts['Engineering']/uni_depts['Enrolled'],3)
uni_depts['Business'] = round(uni_depts['Business']/uni_depts['Enrolled'],3)
uni_depts['Arts'] = round(uni_depts['Arts']/uni_depts['Enrolled'],3)
uni_depts['Science'] = round(uni_depts['Science']/uni_depts['Enrolled'],3)

##Unpivot the enrollment fields into longer shape
uni_depts.drop(columns=['Enrolled'],inplace=True)
uni_depts = uni_depts.melt(id_vars=['Year','Term'],var_name='Department',value_name='Department Share')
uni_depts = uni_depts.sort_values('Year',ascending=True).reset_index(drop=True)
uni_depts['Semester'] =uni_depts['Term']+ ' ' +  uni_depts['Year'].astype(str).str[-2:]

#================================================================================

#App layout
col1, col2 = st.columns(2)

with col1:
  #============================================================
  st.header('Tracking Plots')
  #Admissions tracking dashboard
  fig = go.Figure()

  #Applications line
  fig.add_scatter(x=[uni_data['Year'],uni_data['Term']], y=uni_data['Applications'],
                  mode = 'lines',name='Applications',
                  line=dict(width=3),
                  hovertemplate =
                  '<b>%{x}</b><br>'+
                  '<b># of Applications: </b>%{y}<br>')
  #Admissions line
  fig.add_scatter(x=[uni_data['Year'],uni_data['Term']], y=uni_data['Admitted'],
                  mode = 'lines', name='Admissions',
                  line=dict(width=3),
                  text = uni_data['Admissions Rate (%)'],
                  hovertemplate=
                  '<b>%{x}</b><br>'+
                  '<b>Admitted Students: </b>%{y}<br>'+
                  '<b>Admissions Rate: </b>%{text}%')
  #Enrolled line
  fig.add_scatter(x=[uni_data['Year'],uni_data['Term']], y=uni_data['Enrolled'],
                  mode = 'lines',name='Enrollment',
                  line=dict(width=3),
                  text = uni_data['Matriculation Rate (%)'],
                  hovertemplate=
                  '<b>%{x}</b><br>'+
                  '<b>Enrolled Students: </b>%{y}<br>'+
                  '<b>Matriculation Rate: </b>%{text}%')

  #Add titles and adjust axes
  fig.update_layout(title = 'University Admissions Tracking',
                    title_font_size = 24,
                    width = 600,
                    height = 400)
  fig.update_xaxes(title = 'Semester',
                  title_font_size = 18)
  fig.update_yaxes(title = 'Number of Students',
                  title_font_size = 18,
                  tickformat = ',.0r')

  st.plotly_chart(fig,use_continer_width=True)
  #============================================================
  #Performance Tracking
  metrics_fig1 = go.Figure()

  # Add retention rate
  metrics_fig1.add_trace(go.Scatter(
      x=metrics[metrics['Metric'] == 'Retention Rate']['Year'],
      y=metrics[metrics['Metric'] == 'Retention Rate']['Value'],
      mode='markers+lines',
      name='Retention Rate',
      marker=dict(size=10)
  ))

  #Add satisfaction rate
  metrics_fig1.add_trace(go.Scatter(
      x=metrics[metrics['Metric'] == 'Student Satisfaction']['Year'],
      y=metrics[metrics['Metric'] == 'Student Satisfaction']['Value'],
      mode='markers+lines',
      name='Satisfaction Rate',
      marker=dict(size=10)
  ))

  #Add performance goal level
  metrics_fig1.add_trace(go.Scatter(
      x=metrics['Year'],
      y=np.full(len(metrics['Year']),85),
      mode='lines',
      name='Benchmark',
      line=dict(color='gray', dash='dash',width=4)
  ))

  metrics_fig1.update_layout(
      title='Key Performance Indicators',
      title_font_size=24,
      xaxis=dict(title="Year"),
      yaxis=dict(title="Value"),
      width = 600,
      height = 400)

  metrics_fig1.update_traces(hovertemplate="<br>".join([
      "Year: %{x}",
      "Rate: %{y}"]))

  metrics_fig1.update_xaxes(title = 'Academic Year',
                            title_font_size = 18)

  metrics_fig1.update_yaxes(title = 'Performance Rate (%)',
                            title_font_size = 18,
                            range=[50,100])

  st.plotly_chart(metrics_fig1,use_container_width=True)
  #============================================================

with col2:
  depts_fig = px.bar(uni_depts,x='Semester',y='Department Share',
             color = 'Department',custom_data = 'Department')

  depts_fig.update_traces(hovertemplate="<br>".join([
      'Department: %{customdata[0]}',
      "Semester: %{x}",
      "Department Share: %{y}"]))

  depts_fig.update_layout(title='Department Enrollment Shares',
                          title_font_size = 24,
                          width = 600,
                          height = 400)
  depts_fig.update_xaxes(title='Semester',
                        tickangle=-45)
  depts_fig.update_yaxes(title='Department Share of Enrollment',
                        tickformat='0.0%')
  st.plotly_chart(depts_fig,use_container_width=True)
