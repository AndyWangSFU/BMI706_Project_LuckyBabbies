import altair as alt
import pandas as pd
import streamlit as st
from datetime import datetime, date


st.set_page_config(page_title="Plotting Demo", page_icon="📊")

@st.cache_data
def load_data():
    df = pd.read_csv("users_stat.csv")

    return df

df = load_data()

# st.dataframe(df)

# df = df.fillna(0)
# df.BirthYear.astype(int)

# st.write("# BMI 706 Project ")
# st.write("## Team - LuckyBabies (Fuchen Li, Xi Wang, Zihan Wang)")

# print(df.dtypes)
# st.dataframe(df)

st.write("Please specify the group you are interested in: ")


year = st.slider("Year",int(df["BirthYear"].min()), int(df["BirthYear"].max()), (1927,1986))

# print(year)

# subset = df[((df["BirthYear"] >= year[0]) & (df["BirthYear"] <= year[1])) | (df['BirthYear'].isna())]

subset = df[((df["BirthYear"] >= year[0]) & (df["BirthYear"] <= year[1])) ]

sex = st.radio("Sex", ('All', ' Male', ' Female'))
if sex != 'All':
    subset = subset[subset["Gender"] == sex]




options = st.multiselect(
    'Select medication(s) that you want to subset',
    ['Levadopa', 'DA', 'MAOB', 'Other'],
    [])



if 'Levadopa' in options:
    subset = subset[subset["Levadopav"] == " True"]
if 'DA' in options:
    subset = subset[subset["DA"] == " True"]
if 'MAOB' in options:
    subset = subset[subset["MAOB"] == " True"]
if 'Other' in options:
    subset = subset[subset["Other"] == " True"]



st.write(subset.shape[0], " lines of patient data (out of 227) remain.")


subset2 = subset.groupby(['Parkinsons'])['Parkinsons'].count().to_frame()
subset2["Parkinsons_index"] = subset2.index

# st.dataframe(subset2)


st.write("### Plot 1: Donut Charts of Parkinsons and Tremors ")


chart = alt.Chart(subset2).mark_arc(innerRadius=30).encode(
    theta=alt.Theta(field="Parkinsons", type="quantitative"),
    color=alt.Color(field="Parkinsons_index", type="nominal"),
).properties(
    width=10,
    height=150
)

st.altair_chart(chart, use_container_width=True)


subset3 = subset.groupby(['Tremors'])['Tremors'].count().to_frame()
subset3["Tremors_index"] = subset3.index


chart1 = alt.Chart(subset3).mark_arc(innerRadius=30).encode(
    theta=alt.Theta(field="Tremors", type="quantitative"),
    color=alt.Color(field="Tremors_index", type="nominal", scale=alt.Scale(scheme='dark2')),
).properties(
    width=100,
    height=150
)

st.altair_chart(chart1, use_container_width=True)


def age(born):
    today = date.today()
    return today.year - born
  
subset['Age'] = df['BirthYear'].apply(age)

bins= [30,40,50,60,70,80,90,100]
labels = ['30-40','40-50','50-60','60-70','70-80','80-90','90-100']
subset['AgeGroup'] = pd.cut(subset['Age'], bins=bins, labels=labels, right=False)



subset4 = subset.groupby(['AgeGroup','Gender'], as_index=False)['Parkinsons'].count()

# subset.reset_index(inplace=True)
# st.dataframe(subset4)
# print(subset4)



chart2 = alt.Chart(subset4).mark_bar().encode(
    x='Gender:N',
    y='Parkinsons:Q',
    color='Gender:N',
    column='AgeGroup:N'
).properties(
    width=50,
    height=100
)

st.altair_chart(chart2)



st.write("The whole filtered dataset is: ")

st.dataframe(subset)









