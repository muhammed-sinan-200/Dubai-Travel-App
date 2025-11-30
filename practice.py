import streamlit as st

st.title("Hello from Upcode")

name=st.text_input("Enter your name:")
if st.button("Say hello"):
    st.write(f"Hello, {name} Welcome to UPCODE ")
