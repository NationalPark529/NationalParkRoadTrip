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


#generate advanced options string. At present this doesn't do anything to avoid complicating debugging the back-end

transport_mode = "driving"
avoid_tolls = False
avoid_ferries = False
avoid_highways = False
units = "imperial"

if (st.checkbox("Advanced options")):
    transport_mode = st.radio("Mode of transportation.", ("driving", "flying", "transit"))
    avoid_tolls = st.checkbox("Avoid tolls")
    avoid_ferries = st.checkbox("Avoid ferries")
    avoid_highways = st.checkbox("Avoid highways")
    units = st.radio("Distance Units", ("imperial", "metric"))


avoid_string = ""
if (avoid_tolls):
    avoid_string += "&avoid=tolls"
if (avoid_ferries):
    if (avoid_string == ""):
        avoid_string += "&avoid=ferries"
    else:
        avoid_string += "|ferries"
if (avoid_highways):
    if (avoid_string == ""):
        avoid_string += "&avoid=highways"
    else:
        avoid_string += "|highways"

advanced_configuration = f"&mode={transport_mode}{avoid_string}&units={units}"

#init
if (st.button("Click to optimize!")):
    opt = ParkVRP.ParkVRP(numparks, address)
    list, url = opt.solve()
    for x in url:
        src = f"https://www.google.com/maps/embed/v1/directions?key={st.secrets['GOG_KEY']}&{x}"
        #src = f"https://www.google.com/maps/embed/v1/directions?key={st.secrets['GOG_KEY']}&{x}{advanced_configuration}"
        st.components.v1.iframe(src, width=600, height=450, scrolling=False)

