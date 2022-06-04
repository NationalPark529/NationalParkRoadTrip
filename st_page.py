#from turtle import width
import streamlit as st
import ParkVRP
import ParkInfo

#computation function
def optimize_route(numparks, address):
    #check if the parameters are the same as the last run
    if(st.session_state.numparks == numparks and st.session_state.address == address):
        return st.session_state.list, st.session_state.url
    
    #run the solver
    list, url = st.session_state.opt.solve(numparks, address)
    #This has been throwing a lot of exceptions for me, but I don't know how it works so I can't easily debug it.

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

#initialize the solver and ParkInfo objects for the session-saves a lot of work
if 'opt' not in st.session_state:
    st.session_state.opt = ParkVRP.ParkVRP()
if 'info' not in st.session_state:
    st.session_state.info = ParkInfo.ParkInfo()

#so optimize_route doesn't throw a fit when it tries to access these for the first time
if 'numparks' not in st.session_state:
    st.session_state.numparks = ""
if 'address' not in st.session_state:
    st.session_state.address = ""

if 'list' not in st.session_state:
    st.session_state.list = ""
if 'url' not in st.session_state:
    st.session_state.url = ""

if 'previousPage' not in st.session_state:
    st.session_state.previousPage = "Road Trip Optimizer"

#set up navigation
with st.sidebar:
    displayedPage = st.radio("Page", ("Road Trip Optimizer", "Park Information"))


#Road trip optimizer page
if (displayedPage == "Road Trip Optimizer"):
    #collect routing information
    with st.form("Trip information"):
        #get address
        address = st.text_input("Enter the address you'll be starting your trip from:", value = st.session_state.address)

        #get number of parks
        numparks = st.text_input("How many parks do you want to visit?", value = st.session_state.numparks)
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
    
    #Preserves the page from the last time it was accessed-doesn't preserve any of the 'advanced options' at the moment
    if (st.session_state.previousPage != "Road Trip Optimizer"):
        list, url = optimize_route(numparks, address)


    #display maps and trip information
    if (st.session_state.show_maps):
        with st.expander ("Show parks visited"):
            for trip in list:
                for park in trip:
                    park_info_string = park.park_name + " | ID: " + str(park.park_id)
                    st.write(park_info_string)
        for x in st.session_state.url:
            src = f"https://www.google.com/maps/embed/v1/directions?key={st.secrets['GOG_KEY']}&{x}{advanced_configuration}"
            st.components.v1.iframe(src, width=600, height=450, scrolling=False)
    
    st.session_state.previousPage = "Road Trip Optimizer"



#Park information page-incomplete
elif (displayedPage == "Park Information"):
    info_request_ID = st.text_input("Want to learn more about a specific park? Put its ID here.", value = "0")
    #this is not a good way to implement this from a UI standpoint but I cannot be fucked right now
    try:
        info_request_ID = int(info_request_ID)
    except:
        st.write("Must be an integer")
    if (info_request_ID > 0):
        #currently this just displays the first image available for the park, it's a placeholder for later when I decide to actually put effort into this
        park_information = st.session_state.info.get_park_info(info_request_ID)
        src = park_information["images"][0]["url"]
        st.components.v1.iframe(src, width = 1000, height = 1000, scrolling=True)
    
    st.session_state.previousPage = "Park Information"