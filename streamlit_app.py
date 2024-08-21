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
st.write("Please browse by auction site on the left or use the > symbol at the top if using a phone")
st.write("Remember to check the date, time and location of the auction before setting off")
st.write("Happy house hunting")
#st.write("The generate button will save the auctions to our local server no need to test")
st.write("Check us out at www.aidatalytics.co.uk")
st.write("Give us feedback or make an order contact@aidatalytics.co.uk")
#st.write("Just open the app a few times you should notice that until 14 August that the data may change")
#st.write("Please let us know if the data doesn't change and thanks for helping!")

