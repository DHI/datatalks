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



st.subheader("Bar plots")

# add columns
col1, col2, col3 = st.columns((1, 1, 1))

# Matplotlib
with col1:
    st.write("**Matplotlib**")
    mpl_plot_slot = st.empty()
    with st.echo():
        import matplotlib.pyplot as plt
        plt.hist(df['water level a'], 
                 bins=10, 
                 alpha=0.5, 
                 label='Water level A')
        plt.hist(df['water level b'], 
                 bins=10, 
                 alpha=0.5, 
                 label='Water level B')
        plt.xlabel('Water level')
        plt.ylabel('Frequency')
        plt.legend()
    mpl_plot_slot.pyplot(plt)

# Pandas
with col2:
    st.write("**Pandas plotting**")
    pd_plot_slot = st.empty()
    with st.echo():
        import pandas as pd
        ax = df.plot.hist(alpha=0.5, 
                          bins=10)
        ax.set_xlabel('Water level')
    pd_plot_slot.write(ax.figure)

# Seaborn
with col3:
    st.write("**Seaborn**")
    sns_plot_slot = st.empty()
    with st.echo():
        import seaborn as sns
        sns_plot = sns.histplot(data=df_long, 
                                x='Water level', 
                                hue='Station', 
                                bins=10)
    sns_plot_slot.pyplot(sns_plot.figure)


with st.expander("""**Most important takeaways from "static" libraries**"""):
    st.markdown("""
    * **matplotlib**: separate plotting of histogram for each class, no automatic alignment of bins
    * **pandas**: short code, automatic alignment of bins
    * **seaborn**: all benefits of pandas plus nice styling. Fyi: seaborn has no stacked bar charts
            """)


col4, col5, col6 = st.columns((1, 1, 1))

# Bokeh
with col4:
    st.write("**Bokeh**")
    bk_plot_slot = st.empty()
    with st.echo():
        from bokeh.plotting import figure
        from bokeh.palettes import Set2

        def create_hist_data(data, bins=10):
            hist, edges = np.histogram(data, 
                                       bins=bins)
            return hist, edges

        hist_a, edges_a = create_hist_data(df['water level a'], 
                                           bins=10)
        hist_b, edges_b = create_hist_data(df['water level b'], 
                                           bins=10)

        p = figure(x_axis_label="Water level", 
                   y_axis_label="Frequency", width=570, height=400)

        p.quad(top=hist_a, 
               bottom=0, 
               left=edges_a[:-1], 
               right=edges_a[1:], 
               fill_color=Set2[3][0], 
               line_color="white", 
               alpha=0.5, 
               legend_label='Water level A')
        p.quad(top=hist_b, 
               bottom=0, 
               left=edges_b[:-1], 
               right=edges_b[1:], 
               fill_color=Set2[3][1], 
               line_color="white", 
               alpha=0.5, 
               legend_label='Water level B')
        p.legend.location = "top_right"
    bk_plot_slot.bokeh_chart(p)

# Altair
with col5:
    st.write("**Altair**")
    alt_plot_slot = st.empty()
    with st.echo():
        import altair as alt
        altair_chart = alt.Chart(df_long).mark_bar(opacity=0.5).encode(
            alt.X('Water level:Q', 
                  bin=alt.Bin(maxbins=10)),
            alt.Y('count()', 
                  stack=False),
            alt.Color('Station:N'),
            opacity= alt.value(0.5), 
        ).properties(width=570, height=450)
    alt_plot_slot.altair_chart(altair_chart)


# Plotly Express
with col6:
    st.write("**Plotly Express**")
    pl_plot_slot = st.empty()
    with st.echo():
        import plotly.express as px
        plotly_fig = px.histogram(df_long, 
                                  x='Water level', 
                                  color='Station', 
                                  nbins=10, 
                                  opacity=0.5)
        plotly_fig.update_layout(width=570, height=450)
    pl_plot_slot.plotly_chart(plotly_fig)
with st.expander("""**Most important takeaways from "interactive" libraries**"""):
    st.markdown("""
            * **bokeh**: very flexible, but a lot of work. No alignment, non-intuitive
            * **altair**: aggregation (count) on y-axis from binned x-axis. This can be easily changed (e.g. no barh etc. needed)
            * **plotly**: declarative""")

