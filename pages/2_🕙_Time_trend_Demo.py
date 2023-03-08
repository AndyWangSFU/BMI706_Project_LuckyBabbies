import altair as alt
import pandas as pd
import streamlit as st
from datetime import datetime, date
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="Time trend and response distribution", page_icon="🕙")

@st.cache_data

def load_data():
    plot_1_long = pd.read_csv("plot 1.csv", index_col = 0)
    plot_2 = pd.read_csv("plot 2.csv", index_col = 0)

    return plot_1_long, plot_2

plot_1_long, plot_2 = load_data()

st.write("## Time trend for response time, linked to detailed response time distribution")


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

