import altair as alt
import pandas as pd
import streamlit as st
from datetime import datetime, date
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="Time trend and response distribution", page_icon="🕙")

@st.cache_data

def load_data():
    users_stat = pd.read_csv('demographics.csv', index_col = 0)
    user_data = pd.read_csv('time_data.csv.zip', compression = 'zip', index_col = 0)

    return users_stat, user_data

users_stat, user_data = load_data()

st.write("## Time trend for response time, linked to detailed response time distribution")


# turn the response time variables into numeric type. Then clean the abnormal values
user_data['Hold_Time'] = pd.to_numeric(user_data['Hold_Time'], errors='coerce')
user_data['Latency_Time'] = pd.to_numeric(user_data['Latency_Time'], errors='coerce')
user_data['Flight_Time'] = pd.to_numeric(user_data['Flight_Time'], errors='coerce')
user_data.dropna()
user_data = user_data[(user_data['Hold_Time'] >= 0) & (user_data['Latency_Time'] >= 0) & (user_data['Latency_Time'] >= 0)]

# filter the data. Each participants must have at least 30 days of record. And each experiments day must have at least 30 time stamps. 
selected = user_data.groupby(['User_id']).filter(lambda x: x['Date'].count() > 30)
selected = selected.groupby(['Date']).filter(lambda x: x['Timestamp'].count() > 30)

# group the data by date and id
summary_by_date = selected.groupby(['User_id', 'Date'])[['Hold_Time', 'Latency_Time', 'Flight_Time']].mean().reset_index()

# clean the date attribute
summary_by_date['Date'] = pd.to_datetime(summary_by_date['Date'],format='%y%m%d', errors='coerce')
summary_by_date.dropna()
summary_by_date['Date'] = summary_by_date['Date'] - summary_by_date.groupby('User_id')['Date'].transform('first')
summary_by_date['Date'] = summary_by_date['Date'].dt.total_seconds().astype(int)
summary_by_date['Date']/=86400

# filter the grouped data
summary_by_date = summary_by_date[summary_by_date['Hold_Time'] >= 0]
summary_by_date = summary_by_date[summary_by_date['Latency_Time'] >= 0]
summary_by_date = summary_by_date[summary_by_date['Flight_Time'] >= 0]
summary_by_date = summary_by_date.groupby('Date').filter(lambda x: x['User_id'].count() > 15) # sort out negative or outlier dates


# get the data for the first graph
plot_1 = summary_by_date.groupby('Date')[['Hold_Time', 'Latency_Time', 'Flight_Time']].mean().reset_index()
plot_1 = plot_1.round(3)
# clean the outliers
plot_1 = plot_1[(plot_1['Hold_Time'] < 400) & (plot_1['Latency_Time'] < 400) & (plot_1['Flight_Time'] < 400)]

# turn the data frame into long format for ploting
plot_1_long = pd.melt(
     plot_1, id_vars=['Date'], var_name = 'Response type', value_name = 'Response time'
)

# the upper plot for time line
type_selection = alt.selection_single(
    fields=['Response type'], bind='legend'
)

date_selection = alt.selection_interval(encodings=['x'])

time_trend = alt.Chart(plot_1_long).mark_line().encode(
    x = alt.X ('Date:Q'),
    y = alt.Y('mean(Response time):Q'),
    color = alt.Color('Response type'),
    opacity=alt.condition(type_selection, alt.value(1), alt.value(0.3)),
    tooltip = [
            alt.Tooltip("mean(Response time):Q", title="mean response time (ms)"),
            alt.Tooltip("Date:Q", title="Date since the experiment starts (days)")
        ]
).add_selection(
    type_selection
).add_selection(
    date_selection
).properties(
    width = 1000
)


# get the data for the sub plots
plot_2 = summary_by_date.sample(min(5000,len(summary_by_date)))
plot_2 = plot_2[(plot_2['Hold_Time'] < 400) & (plot_2['Latency_Time'] < 400) & (plot_2['Flight_Time'] < 400)]

# turn the data into categories
plot_2['hold time interval'] = pd.cut(plot_2['Hold_Time'], bins=8, labels=['0-50', '50-100', '100-150', '150-200', '200-250', '250-300', '300-350', '>350'], precision=0)
plot_2['latency time interval'] = pd.cut(plot_2['Latency_Time'], bins=8, labels=['0-50', '50-100', '100-150', '150-200', '200-250', '250-300', '300-350', '>350'], precision=0)
plot_2['flight time interval'] = pd.cut(plot_2['Flight_Time'], bins=8, labels=['0-50', '50-100', '100-150', '150-200', '200-250', '250-300', '300-350', '>350'], precision=0)

# left join, include the Parkinson's status into the table
plot_2 = plot_2.merge(users_stat.iloc[:,[0, 3]], on='User_id', how='left')
plot_2 = plot_2.dropna()


# the second plot
sort_order = ['0-50', '50-100', '100-150', '150-200', '200-250', '250-300', '300-350', '>350']

bar_chart_1 = alt.Chart(plot_2).mark_bar().encode(
    x = alt.X('Parkinsons:N', axis=alt.Axis(labels=False, title = None, ticks = False)),
    y = alt.Y('count()', title="Counts"),
    column= alt.Column('hold time interval', title="Hold time (ms)", spacing = 5, sort = sort_order),
    color = alt.Color('Parkinsons:N', sort = ['True', 'False'])
).add_selection(
    date_selection
).transform_filter(
    date_selection 
).properties(
    height = 200,
    width = 30
)

bar_chart_2 = alt.Chart(plot_2).mark_bar().encode(
    x = alt.X('Parkinsons:N', axis=alt.Axis(labels=False, title = None, ticks = False)),
    y = alt.Y('count()', title="Counts"),
    column= alt.Column('latency time interval', title="Latency time (ms)", spacing = 5, sort = sort_order),
    color = alt.Color('Parkinsons:N', sort = ['True', 'False'])
).add_selection(
    date_selection
).transform_filter(
    date_selection 
).properties(
    height = 200,
    width = 30
)

bar_chart_3 = alt.Chart(plot_2).mark_bar().encode(
    x = alt.X('Parkinsons:N', axis=alt.Axis(labels=False, title = None, ticks = False)),
    y = alt.Y('count()', title="Counts"),
    column= alt.Column('flight time interval', title="Flight time (ms)", spacing = 5, sort = sort_order),
    color = alt.Color('Parkinsons:N', sort = ['True', 'False'])
).add_selection(
    date_selection
).transform_filter(
    date_selection 
).properties(
    height = 200,
    width = 30
)

# bar chart for distribution
bar = alt.hconcat(bar_chart_1, bar_chart_2, bar_chart_3).resolve_scale(
    color='independent'
)


stacked_bar_chart_1 = alt.Chart(plot_2).mark_bar(color = 'black').encode(
    x=alt.X('count()', stack="normalize", title = "proportion of patients"),
    y='Parkinsons',
    color=alt.Color('hold time interval:O', sort = sort_order)
).add_selection(
    date_selection
).transform_filter(
    date_selection 
).properties(
    height = 50,
    width = 250
)

stacked_bar_chart_2 = alt.Chart(plot_2).mark_bar().encode(
    x=alt.X('count()', stack="normalize", title = "proportion of patients"),
    y='Parkinsons',
    color=alt.Color('latency time interval:O', sort = sort_order)
).add_selection(
    date_selection
).transform_filter(
    date_selection 
).properties(
    height = 50,
    width = 250
)

stacked_bar_chart_3 = alt.Chart(plot_2).mark_bar().encode(
    x=alt.X('count()', stack="normalize", title = "proportion of patients"),
    y='Parkinsons',
    color=alt.Color('flight time interval:O', sort = sort_order)
).add_selection(
    date_selection
).transform_filter(
    date_selection 
).properties(
    height = 50,
    width = 250
)

# stacked bar chart 
stacked_bar = alt.hconcat(stacked_bar_chart_1, stacked_bar_chart_2, stacked_bar_chart_3).resolve_scale(
    color='independent'
)


# overall plot
chart = alt.vconcat(time_trend, bar, stacked_bar)

st.altair_chart(chart, use_container_width=True)

