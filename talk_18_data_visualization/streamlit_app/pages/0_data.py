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



# page
st.title("data")
st.write("""Synthetic data is generated for the purpose of this demo. 
         The data is a sine wave with a frequency of 6 hours and is supposed to mimic tidal influenced water levels from two stations. 
         The data is generated in two forms: 
         wide and long. The wide form is the default form in pandas. The long form is a more common form in data science.""")

dcols = st.columns(2)
with dcols[0]:
    st.write("Data in **wide** form")
    st.write(df)
with dcols[1]:
    st.write("Data in **long** form")
    st.write(df_long)

