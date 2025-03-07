#libraries
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

#app title
st.title('University Admissions Tracking')

#data load
uni_data = pd.read_csv('university_student_dashboard_data.csv')
uni_data['Admissions Rate (%)'] = round((uni_data['Admitted']/uni_data['Applications'])*100,0).astype(int)
uni_data['Matriculation Rate (%)'] = round((uni_data['Enrolled']/uni_data['Admitted'])*100,0).astype(int)
uni_data = uni_data.sort_values(['Year','Term'],ascending=[True,True]) #Sort by year + term
uni_data['Semester'] =  uni_data['Year'].astype(str) + ' ' +uni_data['Term'] #Create a semester column and convert to ordered category

#define dataframe of metrics
metrics = uni_data[['Year','Term','Semester','Retention Rate (%)','Student Satisfaction (%)']].copy()
metrics = metrics.melt(id_vars=['Year','Term','Semester'],var_name='Metric',value_name='Value')
metrics['Metric'] = metrics['Metric'].str.replace(' (%)','')

metrics = metrics.groupby(['Year','Metric']).agg({'Value':'mean'}).reset_index()
metrics.head()

#App layout
col1, col2 = st.columns(2)

with col1:
  #============================================================
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
                    title_font_size = 24)
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
  )

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
  st.write('Column 2')
