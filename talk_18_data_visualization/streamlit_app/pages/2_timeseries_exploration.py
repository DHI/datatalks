import streamlit as st
import pandas as pd
import mikeio

# set layout to wide
st.set_page_config(layout="wide")	

# functions
#@st.cache_data()
def read_timeseries():  
    ts_model = mikeio.read('data/UKNS2hdHD27_TS_WL-Germany_20220921-20230101_F012.dfs0', 
                     items="Cuxhaven Steubenhöft: Surface elevation").to_dataframe()
    ts_model.columns = ['model']
    ts_model['time'] = ts_model.index
    
    ts_obs = mikeio.read('data/HydroOnline_Cuxhaven_Steubenhoeft_H.dfs0', 
                         items="H").to_dataframe() - 503.3 # subtract offset pn 503.3
    ts_obs.columns = ['obs']
    ts_obs['time'] = ts_obs.index
    
    # merge ts_obs and ts_model on time
    ts = pd.merge(ts_obs, ts_model, on='time')
    
    # add error column
    ts_err = (ts['obs'] - ts['model']).to_frame()
    ts_err.columns = ['error']
    ts_err["time"] = ts.time   
    # melt to wide form
    ts = ts.melt(id_vars=['time'], var_name='source', value_name='value')
    	
    return ts, ts_err

    
st.header('Timeseries exploration')
st.write("-----")

ts, ts_err = read_timeseries()

# create an expander to show data
with st.expander('Show tabular data'):	
    st.write(ts_err)
    st.write(ts_err.dtypes)


def analyze_timeseries(ts, ts_err):
    import altair as alt
    
    sel_sc = alt.selection_interval(encodings=['x', 'y']) # select x,y area in scatter
    scale = alt.Scale(
        domain=list(ts.source.unique()), 
        range=['#4c78a8', '#f58518']
        )
    c = alt.Color('source:N', scale=scale)
    
    scatter = (alt.Chart(ts)
               .mark_circle()
               .encode(
                   alt.X('source:N')
               )
    )
    
    timeseries = (alt.Chart(ts)
             .mark_line(point=True)
             .encode(
                 alt.X(
                     'time:T'
                     ),
                 alt.Y(
                     'value:Q'
                     ),
                 color=alt.condition(sel_sc, c, alt.value('lightgray')),#'source:N'
                 )
             .properties(width=600, height=400)
             .add_selection(sel_sc)
             #.interactive()
             )
    
    errors = (alt.Chart(ts_err)
              .mark_circle()
              .encode(
                  alt.X('time:T'),
                  alt.Y('error:Q'),
                  color='error:Q',
              )
              .properties(width=600)
              )
    chart = alt.vconcat(timeseries, errors, title="Error analysis")	

    st.altair_chart(chart, use_container_width=True)
    #st.altair_chart(errors, use_container_width=True)
    # top: plot timeseries observed and simulated (as line? does highlighting work here?)
    # below: error over time as points or bars
    # below, right: error distribution as bar / hist, select errors and highlight on timeseries

    # does a scatter observation vs. measurement also make sense here?
    # how do we detect phase shifts? should i just optuna fit this?
analyze_timeseries(ts, ts_err)