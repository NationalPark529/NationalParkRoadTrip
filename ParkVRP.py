import numpy as np
import openrouteservice
import openrouteservice.geocode as g
import openrouteservice.optimization as ors_opt
import pandas as pd
import streamlit as st

class ParkVRP:
    def __init__(self, tripLength, homeAddress):
        self.tripLength = tripLength
        self.homeAddress = homeAddress

    def solve(self):
        #load park data to memory
        parks_df = pd.read_csv("data/NPS_Optimization_Data.csv")

        #hit ORS with string address and return coordinates
        client = openrouteservice.Client(key=st.secrets["ORS_KEY"])
        addressJSON = g.pelias_search(client=client, text=self.homeAddress)
        address_coordinates = addressJSON["features"][0]["geometry"]["coordinates"]

        #create vehicles for each trip
        traveller = [ors_opt.Vehicle(id = 0, start=address_coordinates, end=address_coordinates, capacity=[18])]
        traveller.append(ors_opt.Vehicle(id = 1, start=address_coordinates, end=address_coordinates, capacity=[18]))
        traveller.append(ors_opt.Vehicle(id = 2, start=address_coordinates, end=address_coordinates, capacity=[18]))

        #create jobs for each object
        parks = []
        for index, row in parks_df.iterrows():
            if np.isnan(row["visitor_lon"]):
                continue
            parks.append(ors_opt.Job(id = row["PARK_ID"],  location= [row["visitor_lon"],row["visitor_lat"]], service=round(row["hours_per_visit"]*60*60), amount=[1]))

        #run initial optimization
        results = ors_opt.optimization(client=client, jobs=parks, vehicles=traveller)

        #for all of the returned routes, generate destination object
        trips = []
        for i in range(0,len(results["routes"])):
            parks_in_trip = []
            #no id on start and end
            for j in range(1, len(results["routes"][i]["steps"]) - 1):
                park_name = parks_df[parks_df["PARK_ID"] == results["routes"][i]["steps"][j]["id"]]["PARKNAME"].values[0]
                park_coordinates = results["routes"][i]["steps"][j]["location"]
                park_duration = results["routes"][i]["steps"][j]["service"]
                parks_in_trip.append(Destination(park_id =results["routes"][i]["steps"][j]["id"],park_name=park_name, coordinates = park_coordinates, time_on_site=park_duration))
                print(results["routes"][i]["steps"][j])
            trips.append(parks_in_trip)

        #print results to screen
        for o in trips:
            for park in o:
                print(park.park_name + "," +  str(park.coordinates[0]) + "," + str(park.coordinates[1]))
            print("\n")
        print(trips[0][0].park_name)
        print(results)

        final_results = []
        for t in trips:
            parks = []
            traveller = [ors_opt.Vehicle(id = 0, start=address_coordinates, end=address_coordinates, capacity=[9])]
            traveller.append(ors_opt.Vehicle(id = 1, start=address_coordinates, end=address_coordinates, capacity=[9]))
            traveller.append(ors_opt.Vehicle(id = 2, start=address_coordinates, end=address_coordinates, capacity=[9]))
            for location in t:
                parks.append(ors_opt.Job(id = location.park_id,  location= location.coordinates, service=location.time_on_site, amount=[1]))
            results = ors_opt.optimization(client=client, jobs=parks, vehicles=traveller)

            for i in range(0,len(results["routes"])):
                parks_in_trip = []
                #no id on start and end
                for j in range(1, len(results["routes"][i]["steps"]) - 1):
                    park_name = parks_df[parks_df["PARK_ID"] == results["routes"][i]["steps"][j]["id"]]["PARKNAME"].values[0]
                    park_coordinates = results["routes"][i]["steps"][j]["location"]
                    park_duration = results["routes"][i]["steps"][j]["service"]
                    parks_in_trip.append(Destination(park_id =results["routes"][i]["steps"][j]["id"],park_name=park_name, coordinates = park_coordinates, time_on_site=park_duration))
                    print(results["routes"][i]["steps"][j])

                final_results.append(parks_in_trip)


        final_results = []
        for t in trips:
            parks = []
            traveller = [ors_opt.Vehicle(id = 0, start=address_coordinates, end=address_coordinates, capacity=[3])]
            traveller.append(ors_opt.Vehicle(id = 1, start=address_coordinates, end=address_coordinates, capacity=[3]))
            traveller.append(ors_opt.Vehicle(id = 2, start=address_coordinates, end=address_coordinates, capacity=[3]))
            for location in t:
                parks.append(ors_opt.Job(id = location.park_id,  location= location.coordinates, service=location.time_on_site, amount=[1]))
            results = ors_opt.optimization(client=client, jobs=parks, vehicles=traveller)

            for i in range(0,len(results["routes"])):
                parks_in_trip = []
                #no id on start and end
                for j in range(1, len(results["routes"][i]["steps"]) - 1):
                    park_name = parks_df[parks_df["PARK_ID"] == results["routes"][i]["steps"][j]["id"]]["PARKNAME"].values[0]
                    park_coordinates = results["routes"][i]["steps"][j]["location"]
                    park_duration = results["routes"][i]["steps"][j]["service"]
                    parks_in_trip.append(Destination(park_id =results["routes"][i]["steps"][j]["id"],park_name=park_name, coordinates = park_coordinates, time_on_site=park_duration))
                    print(results["routes"][i]["steps"][j])

                final_results.append(parks_in_trip)

        #print results to screen
        for o in final_results:
            for park in o:
                print(park.park_name + "," +  str(park.coordinates[0]) + "," + str(park.coordinates[1]))
            print("\n")

        urls = []
        for trip in final_results:
            url = f"&origin={self.homeAddress.replace(' ', '+')}&waypoints="
            for park in trip:
                url += f"{park.coordinates[0]},{park.coordinates[1]}|"
            url += f"&origin={self.homeAddress.replace(' ', '+')}"
            urls.append(url)

        return final_results, urls

class Destination:
    def __init__(self, park_id,park_name, coordinates, time_on_site):
        self.park_id = park_id
        self.park_name = park_name
        self.coordinates = coordinates
        self.time_on_site = time_on_site





