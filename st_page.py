import streamlit as st
import ParkVRP
import urllib.request
import json

#computation function
def optimize_route(numparks, address):
    #check if the parameters are the same as the last run
    if(st.session_state.numparks == numparks and st.session_state.address == address):
        return st.session_state.list, st.session_state.url
    
    #run the solver
    list, url = st.session_state.opt.solve(numparks, address)

    #update session state
    st.session_state.numparks = numparks
    st.session_state.address = address
    st.session_state.list = list
    st.session_state.url = url

    #return
    return list, url


#initialize session state

#so the app doesn't try to display the maps on the first run
if 'show_maps' not in st.session_state:
    st.session_state.show_maps = False

#initialize the solver for the session-saves the work of repeatedly reading the csv
if 'opt' not in st.session_state:
    st.session_state.opt = ParkVRP.ParkVRP()

#so optimize_route doesn't throw a fit when it tries to access these for the first time
if 'numparks' not in st.session_state:
    st.session_state.numparks = -1
if 'address' not in st.session_state:
    st.session_state.address = "-"


#collect routing information
with st.form("Trip information"):
    #get root
    address = st.text_input("Enter the address you'll be starting your trip from:")

    #get number of parks
    numparks = st.text_input("How many parks do you want to visit?")
    if (numparks!=""):
        try:
            numparks = int(numparks)
        except:
            st.write("\nPlease enter an integer number.\n")


    #generate advanced options string
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

    advanced_configuration = f"{avoid_string}&units={units}"


    #submit form
    if (st.form_submit_button("Click to optimize!")):
        st.session_state.show_maps = True
        list, url = optimize_route(numparks, address)
        st.session_state.list = list
        st.session_state.url = url


#display maps
if (st.session_state.show_maps):
    for x in st.session_state.url:
        src = f"https://www.google.com/maps/embed/v1/directions?key={st.secrets['GOG_KEY']}&{x}{advanced_configuration}"
        st.components.v1.iframe(src, width=600, height=450, scrolling=False)


#test the nps api

#endpoint = f"https://developer.nps.gov/api/v1/parks?parkCode=VIIS&limit=50&start=0&api_key={st.secrets['NPS_KEY']}"
#HEADERS = {"Authorization":st.secrets['NPS_KEY']}
#req = urllib.request.Request(endpoint,headers=HEADERS)
#content = urllib.request.urlopen(req).read().decode()
#st.write(content)

#st.components.v1.iframe(req, width=600, height=450, scrolling=False)