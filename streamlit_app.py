#app title
st.title('University Admissions Tracking')

#data load
uni_data = pd.read_csv('/content/university_student_dashboard_data.csv')
uni_data['Admissions Rate (%)'] = round((uni_data['Admitted']/uni_data['Applications'])*100,0).astype(int)
uni_data['Matriculation Rate (%)'] = round((uni_data['Enrolled']/uni_data['Admitted'])*100,0).astype(int)

#Sort by year + term
uni_data = uni_data.sort_values(['Year','Term'],ascending=[True,True])

#Create a semester column and convert to ordered category
uni_data['Semester'] =  uni_data['Year'].astype(str) + ' ' +uni_data['Term']


#Add plotly chart
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

st.plotly_chart(fig)
