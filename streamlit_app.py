import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import html
#OneDrive\Desktop\Projects\main>streamlit run Home.py

st.set_page_config(page_title="Property Pulse")

st.title("Home")
st.sidebar.success("Select an auction house")

st.write("This app will update with the latest properties for auction each time it is run")
st.write("The generate button will save the auctions to our local server no need to test")
st.write("We will test that ourselves www.aidatalytics.co.uk")
st.write("Please let us know what you think of the interface, if it works we can add more auction houses!")
st.write("Just open the app a few times you should notice that until 14 August that the data may change")
st.write("Please let us know if the data doesn't change and thanks for helping!")
