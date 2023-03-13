import streamlit as st
import pandas as pd
from pandas_datareader import wb
# set layout to wide
st.set_page_config(layout="wide")	

# functions
@st.cache_data()
def read_data(start=1999, end=2019):  
    """ get water data from world bank and return as pandas dataframe"""
    # check that input start is smaller than end
    if start > end:
        raise ValueError('start must be smaller than end')    
    # use pandas_datareader to get world bank data
    filtered_countries = wb.get_countries()
    # get only countries and rid of regions that are Aggregates
    filtered_countries = filtered_countries[filtered_countries['region'] != 'Aggregates']	
    # rename name column to country
    filtered_countries = filtered_countries.rename(columns={'name': 'country'})	
    # set index of filtered_countries to country
    filtered_countries = filtered_countries.set_index('country')	
    
    indicators = ['ER.H2O.FWTL.K3', 'ER.H2O.FWAG.ZS', 'ER.H2O.FWDM.ZS', 'ER.H2O.FWIN.ZS']
    countries = list(filtered_countries.iso3c.values) 

    # download population data for all countries
    dat_pop = wb.download(indicator='SP.POP.TOTL', country=countries, start=start, end=end, errors='ignore')
    # download data via indicator (id) or 'all' for all indicators
    dat = wb.download(indicator=indicators, country=countries, start=start, end=end, errors='ignore')
    
    # merge dat_pop and dat on country and year
    dat = dat.merge(dat_pop, on=['country', 'year']).dropna()	
    # divide ER.H2O.FWTL.K3 by SP.POP.TOTL to get the per capita value (convert from billion m³ to m³)
    dat['m³ per capita'] = (dat['ER.H2O.FWTL.K3'] * 10**9) / dat['SP.POP.TOTL']
    # rename columns to be more expressive in presentation
    dat.columns = ['H2O withdrawal', 'agriculture', 'domestic', 'industry', 'population', 'per capita']
    # add region as information
    dat = dat.join(filtered_countries.region)	
    # convert region to string
    dat['region'] = dat['region'].astype(str)		
    # convert index "year" to int
    dat.index = dat.index.set_levels(dat.index.levels[1].astype(int), level=1)	
    # sort by region 
    dat = dat.sort_values(by=['region', 'country', 'year'])		
    

    return dat

def plot_year_scatter(dat, year):
    dat_year = dat.iloc[dat.index.get_level_values('year') == year]
    
    # scatter plot
    import plotly.express as px
    fig = px.scatter(dat_year, x="per capita", y="H2O withdrawal", 
                     color="region",
                     size="population", size_max=60,
                     # apply log scale to y axis
                     log_y=True,	
                     range_y=[0.001, 10000],	
                     range_x=[0, 6000],
                     hover_name=dat_year.index.get_level_values('country'))	
    # show figure in streamlit
    st.plotly_chart(fig, use_container_width=True)		
 
def plot_year_altair(dat, year):
    import altair as alt   
    # preprocessing of data
    domains = list(dat.region.unique()) 
    dat_year = dat.iloc[dat.index.get_level_values('year') == year]	
    # drop year column
    dat_year = dat_year.reset_index()#.drop(columns='year')	

    
    # altair scaling and coloring
    scale = alt.Scale(
        domain=domains, 
        range=['#4c78a8', '#f58518', '#e45756', '#72b7b2', '#54a24b', '#eeca3b', '#b279a2', '#ff9da6', '#9d755d', '#bab0ac']
        )
    c = alt.Color('region:N', scale=scale)
    
    # provide some selection options and bidirectional linking
    sel_sc = alt.selection_interval(encodings=['x', 'y']) # select x,y area in scatter
    sel_bar = alt.selection_multi(encodings=["y"])        # select one bar in bar chart
    
    # create scatter plot
    sc = (alt.Chart()
          .mark_point()   # type of plot
          .encode(
              alt.X(
                  "per capita:Q", 
                  title='per capita [m³]',
                  scale=alt.Scale(type='linear', domain=[1,10000])
                  ),
              alt.Y(
                  "H2O withdrawal:Q", 
                  title='H2O withdrawal [bn m³]', 
                  scale=alt.Scale(type='log', domain=[0.001,1000])
                  ), 
              size=alt.Size('population:Q', legend=None),
              color=alt.condition(sel_sc, c, alt.value('lightgray')),
              tooltip=['country:N', 'H2O withdrawal', 'population', 'per capita'],
              )
          .properties(width=600, height=400)
          .add_selection(sel_sc)
          .transform_filter(sel_bar)
          )
    
    # create bar plot
    bar = (alt.Chart()
           .mark_bar()
           .encode(
               alt.X(
                   "mean(per capita):Q",
                   title="mean per capita [m³]",
                   #sort=alt.SortField(field="mean(per capita)", order="descending"),
                   scale=alt.Scale(type='linear', domain=[1,10000])
                   ),
               alt.Y(
                   "region:N",
                   ),
               color=alt.condition(sel_bar, c, alt.value('lightgray'))
               )
           .transform_filter(sel_sc)
           .properties(
               width=600, # same width as scatter plot
               )
           .add_selection(sel_bar)
           )
     
    # combine plots   
    chart = alt.vconcat(sc, bar, data=dat_year, title="Water consumption throughout the world")	
    
    # output in streamlit
    st.altair_chart(chart, use_container_width=True)
    
    
    
st.header('Water usage data exploration')
st.write("-----")

# add year picker
st.sidebar.write('**Select year range**')
start = st.sidebar.selectbox('Start year', range(1999, 2020), index=0)
end = st.sidebar.selectbox('End year', range(1999, 2020), index=20)

dat = read_data(start=start, end=end)
# quick and dirty fix: extract regions for first year as they change over time
#regions = dat.iloc[dat.index.get_level_values('year') == start].region.unique()

# create an expander to show data
with st.expander('Show tabular data'):	
    st.write(dat)



# explore data for a single year
year = st.select_slider('Select year', options=range(1999, 2020))   
#plot_year_scatter(dat, year)    



#@st.cache_data()


plot_year_altair(dat, year)