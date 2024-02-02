import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go
# categorical Data = ['Out/Not Out', 'Against', 'Venue', 'Column1', 'H/A', 'Date', 'Result','Format', 'Man of the Match', 'Captain']

# numerical_Data = ['Score', 'Batting Order', 'Inn.']
st.set_page_config(layout='wide')
image = "371321.jpg"

st.title("Virat Kohli Century Analysis 🏏")
uploaded_file = st.file_uploader("Upoad the File",type=['csv','xlsx'])
if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(('.xls', '.xlsx')):
        data = pd.read_excel(uploaded_file, engine='openpyxl')
    else:
        st.error("Unsupported file type. Please upload a CSV or Excel file.")
        st.stop()
st.image(image,caption="Virat Kohli",use_column_width=True)
st.write("Data: ",data)

st.title('Bar Graph')
df = pd.DataFrame(data)
col_x, col_y = st.columns(2)
selected_columns_out_notout = col_x.selectbox("Out/Not Out",df.columns)
selected_columns_against = col_y.selectbox("Against",df.columns)
try:
    chart_data = df.groupby([selected_columns_out_notout,selected_columns_against]).size().unstack()
    st.bar_chart(chart_data)
except Exception as e:
    st.error(f"Error {e}")
st.write(df)

st.text("")
st.title("Pie Chart")
default_line_columns_cat = ['Out/Not Out', 'Against']
default_line_columns_num = ['Score', 'Batting Order']
selected_columns_pie_chart = st.multiselect('select columns ',df.columns,default=default_line_columns_cat)


for col in selected_columns_pie_chart:
    if col in ['Out/Not Out', 'Against', 'Venue', 'Column1', 'H/A', 'Date', 'Result','Format', 'Man of the Match', 'Captain']:
        fig = px.pie(df,names=col,title=f"Pie chart for {col}")
        st.plotly_chart(fig)

for col in selected_columns_pie_chart:
    if col in ['Score', 'Batting Order', 'Inn.']:
        fig = px.pie(df,values=col,title=f"Pie chart for {col}")
        st.plotly_chart(fig)


st.title('Count Plot')
default_line_columns_0 = ['Out/Not Out', 'Against',]
selected_categorical_columns = st.multiselect("Select categorical columns for count plots", [col for col in df.columns if col not in ['Score', 'Batting Order', 'Inn.']],default=default_line_columns_0)
for col in selected_categorical_columns:
    fig = px.histogram(df, x=col, title=f'Count Plot for {col}')
    st.plotly_chart(fig)


st.title("Scatter Plot")
default_line_columns1 = ['Score', 'Inn.']
selected_numerical_data_scatter = st.multiselect('select numerical Data',['Score', 'Batting Order', 'Inn.'],default=default_line_columns1)
for col in selected_numerical_data_scatter:
    fig = px.scatter(df,x=col,y='Score',color='Against',title=f"Scatter Plot of {col} vs Score")
    st.plotly_chart(fig)


st.title('Line Chart')
default_line_columns = ['Score', 'Inn.']
selected_numerical_data_line = st.multiselect('select numerical data',['Score', 'Batting Order', 'Inn.'],default=default_line_columns)
for col in selected_numerical_data_line:
    fig = px.line(df, x='Date',y=col,color='Against',title=f"Line chart of {col} over time")
    st.plotly_chart(fig)


st.title('Radar Chart')
default_line_columns = ['Score', 'Inn.']
selected_numerical_data_radar = st.multiselect('select the col',['Score', 'Batting Order', 'Inn.'],default=default_line_columns)
fig = go.Figure()
for col in selected_numerical_data_radar:
    fig.add_trace(go.Scatterpolar(
        r = df[col],
        theta = df['Against'],
        fill='toself',
        name=col,
    ))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
        )),
    showlegend=True
)
st.plotly_chart(fig)


st.title('Heat Map')
numrical_col = df.select_dtypes(include=['int','float']).columns
fig = px.imshow(df[numrical_col].corr(),labels=dict(color='Correlation'))
fig.update_layout(height=500,width=700,title='Correaltion HeatMap')
st.plotly_chart(fig)


st.title("Violin Chart")
select_categorical = st.selectbox('select cat data',df.select_dtypes(include='object').columns)
select_numerical = st.selectbox('select num data',df.select_dtypes(include='number').columns)
fig = px.violin(df,x=select_categorical,y=select_numerical,box=True,points='all',
                title=f"Violin Plot: {select_numerical} by {select_categorical}")
st.plotly_chart(fig)