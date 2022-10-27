import streamlit as st

st.title("My first app 👍")
st.markdown("some further **explanation**")

output = st.selectbox("this is a slider",["a", "b", "x"])
st.write(output)

