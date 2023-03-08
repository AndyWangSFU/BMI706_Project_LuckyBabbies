import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Drug Use Demo", page_icon="📊")

@st.cache_data
def load_data():
    users_stat = pd.read_csv('demographics.csv', index_col = 0)
    user_data = pd.read_csv('time_data.csv', index_col = 0, low_memory=False)

    original_data = user_data.copy()
    original_data.head()

    user_data['Hold_Time'] = pd.to_numeric(user_data['Hold_Time'], errors='coerce')
    user_data['Latency_Time'] = pd.to_numeric(user_data['Latency_Time'], errors='coerce')
    user_data['Flight_Time'] = pd.to_numeric(user_data['Flight_Time'], errors='coerce')
    user_data.dropna()

    selected = user_data.groupby(['User_id']).filter(lambda x: x['Date'].count() > 30)
    selected = selected.groupby(['Date']).filter(lambda x: x['Timestamp'].count() > 30)

    summary_by_date = selected.groupby(['User_id', 'Date'])[['Hold_Time', 'Latency_Time', 'Flight_Time']].mean().reset_index()
    summary_by_date = pd.DataFrame(summary_by_date)
    summary_by_date['Date'] = pd.to_datetime(summary_by_date['Date'],format='%y%m%d', errors='coerce')
    summary_by_date['Date'] = summary_by_date['Date'] - summary_by_date.groupby('User_id')['Date'].transform('first')
    summary_by_date = summary_by_date[summary_by_date['Hold_Time'] >= 0]
    summary_by_date = summary_by_date[summary_by_date['Latency_Time'] >= 0]
    summary_by_date = summary_by_date[summary_by_date['Flight_Time'] >= 0]


    filtered = summary_by_date.groupby('Date').filter(lambda x: x['User_id'].count() > 15)

    merged_table = filtered.merge(users_stat, how = "left")



    return merged_table



df = load_data()
st.write("## Hold time by drug uses for Parkinson's patients")


drugs_default = ["Levadopav", "DA", "MAOB", "Other"]
drugs = st.multiselect('Drugs', drugs_default, drugs_default)
if len(drugs) == 0:
    st.write("### Please select one or multiple drugs of interest that patients were taking to begin")
else:
    subset = df
    for i in drugs:
        subset = subset[subset[i] == " True"]
    num_patients = len(subset)
    subset = subset.groupby(['Date', 'Gender', 'Parkinsons'])[['Hold_Time', 'Latency_Time', 'Flight_Time']].mean().reset_index()
    subset['Date'] = subset['Date'].dt.total_seconds().astype(int)
    subset['Date']/=86400
    subset = subset[(subset['Hold_Time'] < 400) & (subset['Latency_Time'] < 400) & (subset['Flight_Time'] < 400)]

    chart1 = alt.Chart(subset).mark_line(point = True).encode(
        x = alt.X('Date:O', title='Days since first recorded (day)'),
        y = alt.Y('Hold_Time:Q', title='Average hold time (ms)'),
        color = alt.Color('Gender:N')
    ).properties(
        title=f"Average Hold Time per Day for Patients taking {drugs}, {num_patients} patients"
    )
    st.altair_chart(chart1, use_container_width=True)

    st.write("### Out of the total patients, the average hold time per day by each of the selected drug(s) is shown:")
    for drug in drugs:
        subset2 = df[df["Parkinsons"] == " True"]
        subset2 = df.groupby(['Date', 'Gender', drug, 'Parkinsons'])[['Hold_Time', 'Latency_Time', 'Flight_Time']].mean().reset_index()
        subset2['Date'] = subset2['Date'].dt.total_seconds().astype(int)
        subset2['Date']/=86400
        subset2 = subset2[(subset2['Hold_Time'] < 400) & (subset2['Latency_Time'] < 400) & (subset2['Flight_Time'] < 400)]
        subChart = alt.Chart(subset2).mark_line(point = True).encode(
            x = alt.X('Date:O', title='Days since first recorded (day)'),
            y = alt.Y('Hold_Time:Q', title='Average hold time (ms)'),
            color = alt.Color(drug)
        ).properties(
            title=f"Average Hold Time per Day for Patients by {drug}'s Status"
        )
        st.altair_chart(subChart, use_container_width=True)
