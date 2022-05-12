import streamlit as st

import ParkVRP
#get root
address = st.text_input("Please enter your address:")

#get number of parks
numparks = st.text_input("How many parks do you want to visit?")
if (numparks!=""):
    try:
        numparks = int(numparks)
    except:
        st.write("\nPlease enter an integer number.\n")


#init
if (st.button("Click to optimize!")):
    opt = ParkVRP.ParkVRP(numparks, address)
    list, url = opt.solve()
    for x in url:
        src = f"https://www.google.com/maps/embed/v1/directions?key={st.secrets['GOG_KEY']}&{x}"
        st.components.v1.iframe(src, width=600, height=450, scrolling=False)

