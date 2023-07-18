## Importing Required Libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import altair as alt
from plotly.subplots import make_subplots

## Improting CSV File
beneficiary = pd.read_csv("benificiary_d.csv")
Prototype = pd.read_csv("Prototype.csv")


## Setting Up Title of Dashboad
st.set_page_config(page_title="Demographic Distribution of CMS Beneficiary Data", layout="wide")
st.markdown(f"<h1 style='text-align: left; color: #00008B; width:1360px; height : 100px '>Demographic Distribution of CMS Beneficiary Data</h1>",unsafe_allow_html=True)

## Filtering Options
with st.sidebar:
    st.markdown(
        '<div style="background-color: #00008B; height: 50px; width: 298px; border-radius: 5px">'
        '<h2 style = "text-align: center; color: white"> Filter </h2>'
        '</div>', unsafe_allow_html=True
    )
    a=['All']          
    options1=st.multiselect('Select age', options=['All'] + list(beneficiary['AGE_INTERVAL'].unique().tolist()),default=a)
    options2=st.multiselect('Select Gender', options=['All'] + list(beneficiary['GENDER'].unique().tolist()),default=a)
    options3=st.multiselect('Select Race', options=['All'] + list(beneficiary['RACE'].unique().tolist()),default=a)
    if 'All' in options1:
             filtered_df = beneficiary
    else:
         filtered_df = beneficiary[beneficiary['AGE_INTERVAL'].isin(options1)]
    
    if 'All' not in options2:
         filtered_df = filtered_df[filtered_df['GENDER'].isin(options2)]
           
    if 'All' not in options3:
            filtered_df = filtered_df[filtered_df['RACE'].isin(options3)]
df = filtered_df.drop_duplicates(subset=["DESYNPUF_ID"], keep='first')

## Statistics
    
style = """
div[data-testid="metric-value-container"] {
    font-size: 2em;
    font-weight: bold;
    color: #ffffff;
}
div[data-testid="metric-delta-container"] {
    font-size: 2rem;
    font-weight: bold;
}
div[data-testid="metric-container"] {
    background-color: #B0C4DE; ## color of no. of unqiue patient
    border-radius: 10px;
    padding: 2em;
}
"""
st.write('<style>{}</style>'.format(style), unsafe_allow_html=True)
st.metric("Number of Unique Patients",f"{len(df['DESYNPUF_ID'].unique())}")

## Individual Graphs
col1, col2 = st.columns(2)
with col1:
    fig = px.histogram(df,
                   x= 'AGE_INTERVAL',
                   text_auto=True,
                   width=400,
                   title = "Age-wise Distribution",
                   height=400
                   
                   )
    st.plotly_chart(fig)
    
    value=df.groupby('RACE')['RACE'].count()
    name=df.groupby('RACE')['RACE'].count().index
    fig1 = px.pie(df, values = value,names=name,title = "Race-wise Distribution", width=400,height = 400)
    fig1.update(layout=dict(title=dict(x=0.1)))
    fig1.update_traces(textposition='inside', textinfo='percent')
    st.plotly_chart(fig1)    
    
with col2:
     
    value=df.groupby('GENDER')['GENDER'].count()
    name=df.groupby('GENDER')['GENDER'].count().index
    chart1 = px.pie(df, values = value,names=name,title = "Gender-wise Distribution",width=400, height = 400)
    chart1.update(layout=dict(title=dict(x=0.1)))
    st.plotly_chart(chart1)
   
# with col4:
    
#     df['value'] = df['AGE_INTERVAL'].value_counts(normalize=True) * 100
#     fig2 = px.bar(df,
#              x='AGE_INTERVAL',
#              y='value',
#              text='value',
#              width=600,
#              title="Age Base Analysis",
#              height=400)
#     fig2.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
#     fig2.update_layout(xaxis_title='Age Interval', yaxis_title='Percentage'
# )
#     st.plotly_chart(fig2)

# Calculate hospitalization rates as percentages
Prototype['COVID 19 Hospitalization Rate in Exposed Population (%)'] = Prototype['COVID 19 Hospitalization Rate in Exposed Population (%)'] / 100
Prototype['COVID 19 Hospitalization Rate in Unexposed Population (%)'] = Prototype['COVID 19 Hospitalization Rate in Unexposed Population (%)'] / 100
# Create stacked bar charts
fig = go.Figure()
fig.add_trace(go.Bar(
    x=Prototype['Month'],
    y=Prototype['COVID 19 Hospitalization Rate in Exposed Population (%)'],
    name='COVID Hospitalization Rate',
    marker_color='orange',
    hovertemplate='COVID 19 Hospitalization Rate in Exposed Population: %{y:.2%}<extra></extra>',
))
fig.add_trace(go.Bar(
    x=Prototype['Month'],
    y=Prototype['COVID 19 Hospitalization Rate in Unexposed Population (%)'],
    name='All Hospitalization Rate',
    marker_color='blue',
    hovertemplate='COVID 19 Hospitalization Rate in Unexposed Population: %{y:.2%}<extra></extra>',
))
# Create line chart
fig.add_trace(go.Scatter(
    x=Prototype['Month'],
    y=Prototype['BA.2 Variant Proportion'],
    name='BA.2 Variant Proportion',
    mode='lines+markers',
    line=dict(color='red'),
    hovertemplate='BA.2 Variant Proportion: %{y}<extra></extra>',
    yaxis='y2',
))
fig.add_trace(go.Scatter(
    x=Prototype['Month'],
    y=Prototype['BA.1 Variant Proportion'],
    name='BA.1 Variant Proportion',
    mode='lines+markers',
    line=dict(color='green'),
    hovertemplate='BA.1 Variant Proportion: %{y}<extra></extra>',
    yaxis='y2',
))
# Configure layout
fig.update_layout(
    barmode='stack',
    title='COVID and All Hospitalization Rates',
    xaxis=dict(title='Month'),
    yaxis=dict(title='Hospitalization Rate (%)', tickformat='%'),
    yaxis2=dict(title='Variant Proportion', overlaying='y', side='right'),
)
# Display the chart using Streamlit
st.plotly_chart(fig, use_container_width=True)

Prototype1 = pd.read_csv("Prototype1.csv")

month_order = ["Jan-22","Feb-22","Mar-22","Apr-22","May-22","Jun-22","Jul-22","Aug-22","Sep-22","Oct-22","Nov-22","Dec-22","Jan-23","Feb-23","Mar-23","Apr-23","May-23","Jun-23"]
    

#######
Prototype1["Month"] = pd.Categorical(Prototype1["Month"], categories=month_order, ordered=True)
Prototype1 = Prototype1.drop(index=Prototype1.index[18:], inplace=False)

# Create line chart for B.1.1.529 variant
fig_variant1 = go.Scatter(x=Prototype1['Month'], y=Prototype1['Variant1'], line=dict(color='red'), name='B.1.1.529 Variant')
fig_variant2 = go.Scatter(x=Prototype1['Month'], y=Prototype1['Variant2'], line=dict(color='blue'), name='BA.1.1 Variant')
fig_variant3 = go.Scatter(x=Prototype1['Month'], y=Prototype1['Variant3'], line=dict(color='green'), name='BA.2 Variant')
fig_variant4 = go.Scatter(x=Prototype1['Month'], y=Prototype1['Variant4'], line=dict(color='grey'), name='BA.2.12.1 Variant')
fig_variant5 = go.Scatter(x=Prototype1['Month'], y=Prototype1['Variant5'], line=dict(color='black'), name='BA.5 Variant')
fig_variant6 = go.Scatter(x=Prototype1['Month'], y=Prototype1['Variant6'], line=dict(color='pink'), name='BQ.1.1 Variant')
fig_variant7 = go.Scatter(x=Prototype1['Month'], y=Prototype1['Variant7'], line=dict(color='orange'), name='XBB.1.5 Variant')

# Create subplot for hospitalization rates
fig_hospitalization = go.Figure()

# Add bar trace for exposed hospitalization rates
fig_exposed = go.Bar(x=Prototype1['Month'], y=Prototype1['COVID 19 Hospitalization Rate in Exposed Population (%)'], opacity=0.4, marker=dict(color='blue'), name='COVID Hospitalization Rate in Exposed Population')
fig_hospitalization.add_trace(fig_exposed)

# Add bar trace for unexposed hospitalization rates
fig_unexposed = go.Bar(x=Prototype1['Month'], y=Prototype1['COVID 19 Hospitalization Rate in Unexposed Population (%)'], opacity=0.4, marker=dict(color='green'), name='COVID Hospitalization Rate in Unexposed Population')
fig_hospitalization.add_trace(fig_unexposed)

# Configure the left y-axis for hospitalization rates
y1_range = [0, 0.05]  # Set the range to 0 to 5% for hospitalization rates
fig_hospitalization.update_layout(yaxis=dict(title='COVID 19 Hospitalization Rate (%)', tickformat=".2%",side='left', range=y1_range, showgrid=True, zeroline=False, showline=True, linewidth=2, linecolor='black', mirror=True)

# Create subplot for variant proportion
fig_combined = make_subplots(specs=[[{"secondary_y": True}]])

# Add line trace for the variant proportion
fig_combined.add_trace(fig_variant1)
fig_combined.add_trace(fig_variant2)
fig_combined.add_trace(fig_variant3)
fig_combined.add_trace(fig_variant4)
fig_combined.add_trace(fig_variant5)
fig_combined.add_trace(fig_variant6)
fig_combined.add_trace(fig_variant7)

# Configure the right y-axis for the variant proportion
y2_range = [0, 50]  # Set the range to 0 to 50 for variant proportion
fig_combined.update_layout(yaxis2=dict(title='Variant Proportion', tickformat="", range=y2_range, overlaying='y', side='right', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black', mirror=True))

# Merge both subplots
fig_combined.update_traces(yaxis='y2')  # Align the variant line chart with the right y-axis
for trace in fig_hospitalization.data:
    fig_combined.add_trace(trace)

# Configure the layout
fig_combined.update_layout(title='COVID Hospitalization Rate & Circulating Variants Over Time', xaxis_title='Month-Year', width=1200, height=600,
                           legend=dict(orientation='h', yanchor='bottom', y=-0.4, xanchor='center', x=0.5),
                           margin=dict(l=50, r=50, t=100, b=80))

# Render the Plotly figure using Streamlit
st.plotly_chart(fig_combined)
