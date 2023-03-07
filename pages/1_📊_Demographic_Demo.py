import altair as alt
import pandas as pd
import streamlit as st


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
subset2["ParkinsonsDisease"] = subset2.index

# st.dataframe(subset2)



chart = alt.Chart(subset2).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="Parkinsons", type="quantitative"),
    color=alt.Color(field="ParkinsonsDisease", type="nominal"),
).properties(
    width=100,
    height=200
)

st.altair_chart(chart, use_container_width=True)


st.write("The whole filtered dataset is: ")

st.dataframe(subset)









