import streamlit as st
import pandas as pd

import numpy as np
from datetime import timedelta
st.set_page_config(layout="wide")	


# -------------------------------------- data --------------------------------------
def create_water_levels_dataframe(frequency_hours, amplitude_deviation=0.2):
    start_date = pd.to_datetime('2023-01-06')
    end_date = pd.to_datetime('2023-01-13')
    delta = timedelta(minutes=10)
    datetime_index = pd.date_range(start_date, end_date, freq=delta)
    num_periods = len(datetime_index)
    frequency_a = 2 * np.pi / (frequency_hours * 60 / 10)  # Given frequency in hours, 10-minute intervals
    frequency_b = frequency_a * 1.003  # Slightly different frequency for water level b

    water_level_a = np.sin(frequency_a * np.arange(num_periods)) * (1 + np.random.normal(0, amplitude_deviation, num_periods))
    water_level_b = np.sin(frequency_b * np.arange(num_periods)) * (1 + np.random.normal(0, amplitude_deviation, num_periods))
    df = pd.DataFrame(
        data={"water level a": water_level_a, "water level b": water_level_b},
        index=datetime_index
    )

    return df

frequency_hours = 6
df = create_water_levels_dataframe(frequency_hours)
df.name = 'Date'

df_long = df.reset_index().melt(id_vars='index', var_name='Station', value_name='Water level')
df_long.rename(columns={'index': 'Date'}, inplace=True)



st.subheader("Line plots")

# add columns
col1, col2, col3 = st.columns((1,1,1))	

# Matplotlib
with col1:
    st.write("**Matplotlib**")
    mpl_plot_slot = st.empty()
    with st.echo():
        import matplotlib.pyplot as plt
        plt.plot(df, 
                 label=['water level a', 
                        'water level b']) # labeling needed
        plt.xlabel('Date')
        plt.ylabel('Water level')
        plt.legend()
    mpl_plot_slot.pyplot(plt)

# Pandas
with col2:
    st.write("**Pandas plotting**")
    pd_plot_slot = st.empty()
    with st.echo():
        import pandas as pd
        ax = df.plot(
            xlabel='Date', 
            ylabel='Water level')
    pd_plot_slot.write(ax.figure)

# Seaborn
with col3:
    st.write("**Seaborn**")
    sns_plot_slot = st.empty()
    with st.echo():
        import seaborn as sns
        sns_plot = sns.lineplot(data=df_long)
        handles, labels = sns_plot.get_legend_handles_labels() # if not removed, sns will create legend for Value column
        sns_plot.legend(handles=handles[:-1], labels=labels[:-1])
    sns_plot_slot.pyplot(sns_plot.figure)


with st.expander("""**Most important takeaways from "static" libraries**"""):
    st.markdown("""
            * **matplotlib**: no native datetime support, most "manual" labor needed.
            * **pandas**: good x-limits, automatic legend generation
            * **seaborn**: automatic x,y labelling. Very similar to pandas (can handle long and wide format but former is preferred). 
            """)



col4, col5, col6 = st.columns((1,1,1))

# Bokeh
with col4:
    st.write("**Bokeh**")
    bk_plot_slot = st.empty()
    with st.echo():
        from bokeh.plotting import figure
        p = figure(x_axis_type="datetime", 
                   x_axis_label="Date", 
                   y_axis_label="Water Level", width=570, height=400)
        p.line(df.index, df['water level a'], # using df more concise here
               legend_label='water level a', line_color="orange")
        p.line(df.index, df['water level b'], 
               legend_label='water level b', line_color="#1f77b4")
        # for notebook plots we might have to force rendering in notebook instead of in browser
    bk_plot_slot.bokeh_chart(p)

# Altair
with col5:
    st.write("**Altair**")
    alt_plot_slot = st.empty()
    with st.echo():
        import altair as alt
        altair_chart = alt.Chart(df_long).mark_line().encode(
            x='Date:T',
            y='Water level:Q',
            color='Station:N').properties(width=570, height=450)
    alt_plot_slot.altair_chart(altair_chart)

# Plotly
with col6:
    st.write("**Plotly**")
    pl_plot_slot = st.empty()
    with st.echo():
        import plotly.express as px
        plotly_fig = px.line(df_long, 
                             x='Date', 
                             y='Water level', 
                             color='Station')
        plotly_fig.update_layout(width=570, height=450)
    pl_plot_slot.plotly_chart(plotly_fig)
    
    
with st.expander("""**Most important takeaways from "interactive" libraries**"""):
    st.markdown("""
            * **bokeh**: while very flexible (low to high level interface) and interactive it is a lot of work (e.g. seperate definition of lines)
            * **altair**: declarative i) handing over data, ii) chosing mark, iii) chosing encoding (what goes where) iv) adding interactivity etc.
            * **plotly**: declarative, very similar to altair here
            * all support exports of figures (sometimes only png, others also vector graphics)
            """)