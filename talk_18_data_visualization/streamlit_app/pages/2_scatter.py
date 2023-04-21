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



st.subheader("Scatter plots")

# add columns
col1, col2, col3 = st.columns((1, 1, 1))

# Matplotlib
with col1:
    st.write("**Matplotlib**")
    mpl_plot_slot = st.empty()
    with st.echo():
        import matplotlib.pyplot as plt
        plt.scatter(df['water level a'], 
                    df['water level b'])
        plt.xlabel('water level A')
        plt.ylabel('water level B')
    mpl_plot_slot.pyplot(plt)

# Pandas
with col2:
    st.write("**Pandas plotting**")
    pd_plot_slot = st.empty()
    with st.echo():
        import pandas as pd
        ax = df.plot.scatter(x='water level a', 
                             y='water level b') 
    pd_plot_slot.write(ax.figure)

# Seaborn
with col3:
    st.write("**Seaborn**")
    sns_plot_slot = st.empty()
    with st.echo():
        import seaborn as sns
        sns_plot = sns.scatterplot(data=df, 
                                   x='water level a', 
                                   y='water level b')
    sns_plot_slot.pyplot(sns_plot.figure)
    

with st.expander("""**Most important takeaways from "static" libraries**"""):
    st.markdown("""
            * **matplotlib**: most "manual" labor needed.
            * **pandas**: automatic axis labels
            * **seaborn**: very brief code and nice default styling. Can handle coloring of classes very well (not shown here).

            """)



col4, col5, col6 = st.columns((1, 1, 1))

# Bokeh
with col4:
    st.write("**Bokeh**")
    bk_plot_slot = st.empty()
    with st.echo():
        from bokeh.plotting import figure
        p = figure(x_axis_label="water level a", 
                   y_axis_label="water level b", width=570, height=400)
        p.scatter(df['water level a'], 
                  df['water level b'])
    bk_plot_slot.bokeh_chart(p)

# Altair
with col5:
    st.write("**Altair**")
    alt_plot_slot = st.empty()
    with st.echo():
        import altair as alt
        altair_chart = alt.Chart(df).mark_circle().encode(
            x='water level a:Q',
            y='water level b:Q'
        ).properties(width=570, height=450)
    alt_plot_slot.altair_chart(altair_chart)

# Plotly Express
with col6:
    st.write("**Plotly Express**")
    pl_plot_slot = st.empty()
    with st.echo():
        import plotly.express as px
        plotly_fig = px.scatter(df, 
                                x='water level a', 
                                y='water level b')
        plotly_fig.update_layout(width=570, height=450)
    pl_plot_slot.plotly_chart(plotly_fig)
    
with st.expander("""**Most important takeaways from "interactive" libraries**"""):
    st.markdown("""
            * **Altair and Plotly**: very similar (declarative) syntax.

            """)