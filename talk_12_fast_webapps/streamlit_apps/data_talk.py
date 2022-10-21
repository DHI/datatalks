import streamlit as st
from streamlit_option_menu import option_menu


st.set_page_config(page_title="Data Talk 12",
                   page_icon="🚀",
                   layout="wide")



with st.sidebar:
    selected = option_menu(
        menu_title = "Agenda",
        menu_icon= "list",
        options = ["title", "introduction", 
                   "technology", "benefits", 
                   "example", "what else"],
        icons = ["house", "123", 
                 "gear", "emoji-smile", 
                 "code-slash", "eyeglasses"],
        orientation='vertical'
    )



if selected == "title":
    st.title("Data Talk 12: Quickly create webapps wit Streamlit")
    st.subheader("Paul Daniel & Clemens Cremer")
    
    st.write("DHI T&I - Data & Analytics")



if selected == "introduction":
    if 'page' not in st.session_state:
        st.session_state['page'] = 0

    def increase_page():
        if st.session_state.page < 2: 
	        st.session_state.page += 1
    def decrease_page():
        if st.session_state.page > 0: 
            st.session_state.page -= 1
            
    
    st.title("General introduction: Why (web)apps?")

    if st.session_state.page == 0:
        st.subheader("Do you sometimes feel you could use and present your python work more efficiently as an app?")
        st.markdown("""
                    For instance to:             
                    - create (easily reusable) data exploration 
                    - share your vision, 
                        - e.g. quickly prototype a tool to discuss and narrow down requirements and do **fast iterations in development** or 
                        - **convince people** of tools usefulness 
                    - to provide access to your tools for non-python users?>  
                    
                    -----                  
                    """)
    if st.session_state.page == 1:
        st.subheader("What prevented you?")
        st.markdown("""
                    - you might **lack experience in front-end development** and associated frameworks (such as React, Svelte or Angular), needed to convert your scripts to apps.
                    - **development too time consuming**
                    
                    -----
                    """)
        
    if st.session_state.page == 2:    
        st.subheader("What could solve this?")
        st.markdown("""
                    **Streamlit** provides a very simple way to deploy pure python code as (web)app.
                    
                    -----
                    """)
    
    c1, c2, c3, c4 = st.columns([4,.3,.3,4])        
    c2.button('<', on_click=decrease_page)
    c3.button('>', on_click=increase_page)


if selected == "technology":
    if 'paget' not in st.session_state:
        st.session_state['paget'] = 0

    def increase_paget():
        if st.session_state.paget < 1: 
	        st.session_state.paget += 1
    def decrease_paget():
        if st.session_state.paget > 0: 
            st.session_state.paget -= 1
    
    
    st.title("What is Streamlit?")
 
    if st.session_state.paget == 0: 
        st.subheader("Definition, history and features")  
        st.markdown("""
                    \"*Streamlit is an **open-source Python library** that 
                    makes it easy to create and share beautiful, custom 
                    web apps for machine learning and data science. 
                    In just a few minutes you can build and deploy powerful 
                    data apps.*\" [1](https://docs.streamlit.io/)
                    
                    -----
                    """)
        
        st.markdown("""
                    - python library (installation via pip install, requires python ≥ 3.6)
                    - developed by former Google X people & Carnegie Mellon University (launch ~2020)
                    - open source
                    - Tons of pre-defined components to make your apps beautiful and interactive
                    - Text Formatting in Markdown, HTML, LaTeX 
                    - advanced features: easy caching 
                    -----
                    """)

    if st.session_state.paget == 1:    

        st.subheader("How can I deploy apps?")
        st.markdown("""
                    - locally
                    - streamlit cloud (free, 3 apps max., open)
                    - azure webapps (~10 €/mo)
                    - ....
                    """)

    c1t, c2t, c3t, c4t = st.columns([4,.3,.3,4])        
    c2t.button('<', on_click=decrease_paget)
    c3t.button('>', on_click=increase_paget)    
    
    
if selected == "benefits":
    st.title("Why should I use Streamlit?")
    
    st.subheader("Because it is...")    
    st.markdown("""
                - **very easy** to build (coming from python).
                - the **fastest way to build and deploy** an app
                - **easy to customize** (e.g. with themes and icons)
                - quickly **maturing and expanding**
                
                - **popular**.
                - it has a **large community**
                - Trusted by over 50% of Fortune 50 companies (e.g. Apple, Johnson & Johnson, Wells Fargo, GE, Tesla, Walmart, IBM, ...)
                """)
    
    with st.expander(label="Let's see how it compares to other plotting frameworks"):
        tscale = st.selectbox("Select time-axis", ["Date", "Timeline"])
        st.markdown(f"[![Star History Chart](https://api.star-history.com/svg?repos=streamlit/streamlit,bokeh/bokeh,plotly/dash,voila-dashboards/voila,rstudio/shiny,jupyter/notebook&type={tscale})](https://star-history.com/#streamlit/streamlit&bokeh/bokeh&plotly/dash&voila-dashboards/voila&rstudio/shiny&jupyter/notebook&{tscale})")

  
 
if selected == "example":
    st.title("Basic example")
    
    st.markdown("""
                In this example we will:\n
                0. import streamlit
                1. write header
                2. make interactive element
                3. get output from interactive element
                4. write output 
                5. modify: e.g. change to slider to selectbox and put in sidebar
                """)


if selected == "what else":
    st.title("What else?")
    
    st.subheader("How is it distinct from Jupyter Notebooks?")
    st.markdown("""
            *\"Streamlit is a full data dashboarding solution, while Jupyter Notebooks
            are primarily useful to engineers who want to develop software and 
            visualizations. Engineers use Streamlit to build dashboards for 
            non-technical users, and they use Jupyter Notebooks to develop code and 
            share it with other engineers.\"* 
            [2](https://www.datarevenue.com/en-blog/data-dashboarding-streamlit-vs-dash-vs-shiny-vs-voila#:~:text=Streamlit%20is%20a%20full%20data,share%20it%20with%20other%20engineers)    
            
            """)    
    
    st.subheader("advanced benefits")
    st.markdown("""
            - dynamic scaling, working well on phones etc.    
            - customizable themes
            - opengl plotting
            - caching, session states and callback functions
            - audio (player) support
            - video (player) support
            -----
            """)

    st.subheader("What's next?")            
    st.markdown("""
            get started
            - by browsing [gallery](https://streamlit.io/gallery)
            - by using [cheat sheet](https://daniellewisdl-streamlit-cheat-sheet-app-ytm9sg.streamlitapp.com/)
            - looking at talks e.g. [Snowflake Build virtual conference](https://www.snowflake.com/build/)
            
            """)

