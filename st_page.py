import streamlit as st
import pandas as pd

import ParkVRP
#get root
address = st.text_input("Please enter your address:")

#get time gone
time = st.text_input("How many parks do you want to visit?")
if (time!=""):
    try:
        time = int(time)
    except:
        st.write("\nPlease enter an integer number.\n")


#init
if (st.button("Click to optimize!")):
    opt = ParkVRP.ParkVRP(time, address)
    list, url = opt.solve()
    src = f"https://www.google.com/maps/embed/v1/directions?key={st.secrets['GOG_KEY']}&{url[0]}"
    st.components.v1.iframe(src, width=600, height=450, scrolling=False)

#config and secrets file