import pandas as pd
import streamlit as st
import urllib
import json

class ParkInfo:
    #initialization. This can take a bit of time.
    def __init__(self):
        #Grab park unit codes from the csv
        parks_df = pd.read_csv("data/NPS_Optimization_Data.csv")
        request_string = ""
        for unit_code in parks_df["UNIT_CODE"]:
            request_string = request_string + unit_code + ","
        request_string = request_string[:-1]

        #API request call
        self.parks_list = self.API_request(request_string)

    #mostly a helper function for __init__, but it works on its own as well
    def API_request(self, unit_codes):
        endpoint = f"https://developer.nps.gov/api/v1/parks?parkCode={unit_codes}&limit=50&start=0&api_key={st.secrets['NPS_KEY']}"
        HEADERS = {"Authorization":st.secrets['NPS_KEY']}
        req = urllib.request.Request(endpoint,headers=HEADERS)
        content = urllib.request.urlopen(req).read().decode()
        park_info = json.loads(content)
        return park_info

    #Returns the dictionary for a particular park, determined by its ID. Probably not permanent in this form
    def get_park_info(self, info_ID):
        return self.parks_list['data'][info_ID]