import streamlit as st
import ParkVRP

#initialize session state
if 'show_maps' not in st.session_state:
    st.session_state['show_maps'] = False

#cached computation function
@st.cache
def optimize_route(numparks, address):
    opt = ParkVRP.ParkVRP(numparks, address)
    list, url = opt.solve()
    return list, url

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