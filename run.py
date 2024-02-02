import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
# categorical Data = ['Out/Not Out', 'Against', 'Venue', 'Column1', 'H/A', 'Date', 'Result','Format', 'Man of the Match', 'Captain']

# numerical_Data = ['Score', 'Batting Order', 'Inn.']

st.title("Virat Century Analysis")
uploaded_file = st.file_uploader("Upoad the File",type=['csv','xlsx'])
if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(('.xls', '.xlsx')):
        data = pd.read_excel(uploaded_file, engine='openpyxl')
    else:
        st.error("Unsupported file type. Please upload a CSV or Excel file.")
        st.stop()
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
selected_columns_pie_chart = st.multiselect('select columns ',df.columns)

# for col in selected_columns_pie_chart:
#     if col in ['Out/Not Out', 'Against', 'Venue', 'Column1', 'H/A', 'Date', 'Result','Format', 'Man of the Match', 'Captain']:
#         fig,ax = plt.subplots()
#         ax.pie(df[col].value_counts(),labels=df[col].value_counts().index,autopct='%1.1f%%',startangle=90, wedgeprops=dict(width=0.4))
#         ax.set_title(f'pie chart for {col}')
#         ax.axis('equal')
#         st.pyplot(fig)
# for col in selected_columns_pie_chart:
#     if col in ['Score', 'Batting Order', 'Inn.']:
#         fig,ax = plt.subplots()
#         ax.pie(df[col].value_counts(),labels=df[col].value_counts().index,autopct='%1.1f%%',startangle=90, wedgeprops=dict(width=0.4))
#         ax.set_title(f'pie chart for {col}')
#         ax.axis('equal')
#         st.pyplot(fig)
for col in selected_columns_pie_chart:
    if col in ['Out/Not Out', 'Against', 'Venue', 'Column1', 'H/A', 'Date', 'Result','Format', 'Man of the Match', 'Captain']:
        fig = px.pie(df,names=col,title=f"Pie chart for {col}")
        st.plotly_chart(fig)

for col in selected_columns_pie_chart:
    if col in ['Score', 'Batting Order', 'Inn.']:
        fig = px.pie(df,values=col,title=f"Pie chart for {col}")
        st.plotly_chart(fig)

st.title('Count Plot')
selected_categorical_columns = st.multiselect("Select categorical columns for count plots", [col for col in df.columns if col not in ['Score', 'Batting Order', 'Inn.']])
for col in selected_categorical_columns:
    fig = px.histogram(df, x=col, title=f'Count Plot for {col}')
    st.plotly_chart(fig)
