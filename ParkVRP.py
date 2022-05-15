import numpy as np
import openrouteservice
import openrouteservice.geocode as g
import openrouteservice.optimization as ors_opt
import openrouteservice.distance_matrix as ors_matrix
import pandas as pd
import streamlit as st
from ortools.constraint_solver import routing_enums_pb2, pywrapcp


def print_solution(num_vehicles, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    max_route_distance = 0
    for vehicle_id in range(num_vehicles):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += '{}\n'.format(manager.IndexToNode(index))
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    print('Maximum of the route distances: {}m'.format(max_route_distance))


class ParkVRP:
    def __init__(self,numParks, homeAddress):
        self.numParks = numParks
        self.homeAddress = homeAddress

    #def solve(self):
        #load park data to memory
        #parks_df = pd.read_csv("data/NPS_Optimization_Data.csv")

        #hit ORS with string address and return coordinates
        #client = openrouteservice.Client(key=st.secrets["ORS_KEY"])
        #addressJSON = g.pelias_search(client=client, text=self.homeAddress)
        #address_coordinates = addressJSON["features"][0]["geometry"]["coordinates"]

        #create vehicles for each trip
        #traveller = [ors_opt.Vehicle(id = 0, start=address_coordinates, end=address_coordinates, capacity=[18])]
        #traveller.append(ors_opt.Vehicle(id = 1, start=address_coordinates, end=address_coordinates, capacity=[18]))
        #traveller.append(ors_opt.Vehicle(id = 2, start=address_coordinates, end=address_coordinates, capacity=[18]))

        #create jobs for each object
        #parks = []
        #for index, row in parks_df.iterrows():
        #    if np.isnan(row["visitor_lon"]):
        #        continue
        #    parks.append(ors_opt.Job(id = row["PARK_ID"],  location= [row["visitor_lon"],row["visitor_lat"]], service=round(row["hours_per_visit"]*60*60), amount=[1]))

        #run initial optimization
        #results = ors_opt.optimization(client=client, jobs=parks, vehicles=traveller)

        #for all of the returned routes, generate destination object
        #trips = []
        #for i in range(0,len(results["routes"])):
        #    parks_in_trip = []
            #no id on start and end
        #    for j in range(1, len(results["routes"][i]["steps"]) - 1):
        #        park_name = parks_df[parks_df["PARK_ID"] == results["routes"][i]["steps"][j]["id"]]["PARKNAME"].values[0]
        #        park_coordinates = results["routes"][i]["steps"][j]["location"]
        #        park_duration = results["routes"][i]["steps"][j]["service"]
        #        parks_in_trip.append(Destination(park_id =results["routes"][i]["steps"][j]["id"],park_name=park_name, coordinates = park_coordinates, time_on_site=park_duration))
        #        print(results["routes"][i]["steps"][j])
        #    trips.append(parks_in_trip)

        #print results to screen
        #for o in trips:
        #    for park in o:
        #        print(park.park_name + "," +  str(park.coordinates[0]) + "," + str(park.coordinates[1]))
        #    print("\n")
        #print(trips[0][0].park_name)
        #print(results)

        #final_results = []
        #for t in trips:
        #    parks = []
        #    traveller = [ors_opt.Vehicle(id = 0, start=address_coordinates, end=address_coordinates, capacity=[9])]
        #    traveller.append(ors_opt.Vehicle(id = 1, start=address_coordinates, end=address_coordinates, capacity=[9]))
        #    traveller.append(ors_opt.Vehicle(id = 2, start=address_coordinates, end=address_coordinates, capacity=[9]))
        #    for location in t:
        #        parks.append(ors_opt.Job(id = location.park_id,  location= location.coordinates, service=location.time_on_site, amount=[1]))
        #    results = ors_opt.optimization(client=client, jobs=parks, vehicles=traveller)

        #    for i in range(0,len(results["routes"])):
        #        parks_in_trip = []
                #no id on start and end
        #        for j in range(1, len(results["routes"][i]["steps"]) - 1):
        #            park_name = parks_df[parks_df["PARK_ID"] == results["routes"][i]["steps"][j]["id"]]["PARKNAME"].values[0]
        #            park_coordinates = results["routes"][i]["steps"][j]["location"]
        #            park_duration = results["routes"][i]["steps"][j]["service"]
        #            parks_in_trip.append(Destination(park_id =results["routes"][i]["steps"][j]["id"],park_name=park_name, coordinates = park_coordinates, time_on_site=park_duration))
        #            print(results["routes"][i]["steps"][j])

        #        final_results.append(parks_in_trip)


        #final_results = []
        #for t in trips:
        #    parks = []
        #    traveller = [ors_opt.Vehicle(id = 0, start=address_coordinates, end=address_coordinates, capacity=[3])]
        #    traveller.append(ors_opt.Vehicle(id = 1, start=address_coordinates, end=address_coordinates, capacity=[3]))
        #   traveller.append(ors_opt.Vehicle(id = 2, start=address_coordinates, end=address_coordinates, capacity=[3]))
         #   for location in t:
        #        parks.append(ors_opt.Job(id = location.park_id,  location= location.coordinates, service=location.time_on_site, amount=[1]))
        #    results = ors_opt.optimization(client=client, jobs=parks, vehicles=traveller)

        #    for i in range(0,len(results["routes"])):
        #        parks_in_trip = []
                #no id on start and end
        #        for j in range(1, len(results["routes"][i]["steps"]) - 1):
        #            park_name = parks_df[parks_df["PARK_ID"] == results["routes"][i]["steps"][j]["id"]]["PARKNAME"].values[0]
        #            park_coordinates = results["routes"][i]["steps"][j]["location"]
        #            park_duration = results["routes"][i]["steps"][j]["service"]
        #            parks_in_trip.append(Destination(park_id =results["routes"][i]["steps"][j]["id"],park_name=park_name, coordinates = park_coordinates, time_on_site=park_duration))
         #           print(results["routes"][i]["steps"][j])

         #       final_results.append(parks_in_trip)

        #print results to screen
        #for o in final_results:
        #    for park in o:
        #        print(park.park_name + "," +  str(park.coordinates[0]) + "," + str(park.coordinates[1]))
        #    print("\n")

        #urls = []
        #for trip in final_results:
        #    url = f"&origin={self.homeAddress.replace(' ', '+')}&waypoints="
        #    for park in trip:
        #        url += f"{park.coordinates[1]},{park.coordinates[0]}|"
        #    url = url.rstrip(url[-1])
        #    url += f"&destination={self.homeAddress.replace(' ', '+')}"
        #    urls.append(url)

        #return final_results, urls

    def solve(self):
            #load park data
            parks_df = pd.read_csv("data/NPS_Optimization_Data.csv")

            #hit ORS with string address and return coordinates
            client = openrouteservice.Client(key=st.secrets["ORS_KEY"])
            addressJSON = g.pelias_search(client=client, text=self.homeAddress)
            address_coordinates = addressJSON["features"][0]["geometry"]["coordinates"]

            #create list of locations [lng,lat]
            locations = []
            locations.append(address_coordinates)
            for index, row in parks_df.iterrows():
                if np.isnan(row["visitor_lon"]):
                    continue
                locations.append([row["visitor_lon"],row["visitor_lat"]])

            #Query distance matrix
            distance_matrix = ors_matrix.distance_matrix(client, locations=locations, metrics = ["distance", "duration"])

            #retrieve distance matrix only from response object
            distance_matrix= distance_matrix["distances"]

            #Calculate appropriate number of 'vehicles' in problem  (trip)
            #+1 ensures that there will always be adequate capacity in case of rounding down.
            vehicleNumber = int(50/self.numParks) + 1

            #index of depot (user address) in distance matrix
            depot = 0

            # Create the routing index manager
            manager = pywrapcp.RoutingIndexManager(len(distance_matrix),
                                           vehicleNumber, depot)
            # Create Routing Model.
            routing = pywrapcp.RoutingModel(manager)


            # Create and register a transit callback.
            def distance_callback(from_index, to_index):
                """Returns the distance between the two nodes."""
                # Convert from routing variable Index to distance matrix NodeIndex.
                from_node = manager.IndexToNode(from_index)
                to_node = manager.IndexToNode(to_index)
                return distance_matrix[from_node][to_node]

            transit_callback_index = routing.RegisterTransitCallback(distance_callback)

            # Define cost of each arc. (distance)
            routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

            # Add Distance constraint.
            dimension_name = 'Distance'
            routing.AddDimension(
                transit_callback_index,
                0,  # no slack
                100000000,  # vehicle maximum travel distance
                True,  # start cumul to zero
                dimension_name)

            distance_dimension = routing.GetDimensionOrDie(dimension_name)
            distance_dimension.SetGlobalSpanCostCoefficient(100)


            # SEARCH PARAMETERS
            search_parameters = pywrapcp.DefaultRoutingSearchParameters()

            #Heuristic for finding starting place
            search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.LOCAL_CHEAPEST_INSERTION)
            #Solution Metaheuristic
            search_parameters.local_search_metaheuristic = (
                routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
            )

            #Search limits
            search_parameters.time_limit.seconds = 60
            search_parameters.solution_limit = 100

            #For debugging
            search_parameters.log_search = True

            #add capacity constraint
            def demand_callback(from_index):
                """Returns the demand of the node."""
             #   Demand is always 1
                return 1

            #Create vehicle capacities (+1)
            capacities = []
            for i in range(0, vehicleNumber):
                capacities.append(self.numParks + 1)

            print(capacities)

            demand_callback_index = routing.RegisterUnaryTransitCallback(
            demand_callback)
            routing.AddDimensionWithVehicleCapacity(
                demand_callback_index,
                0,  # null capacity slack
                capacities,  # vehicle maximum capacities
                True,  # start cumul to zero
                'Capacity')

            # Solve the problem.
            solution = routing.SolveWithParameters(search_parameters)

            # Print solution to Console
            if solution:
                print_solution(vehicleNumber, manager, routing, solution)
            else:
                print('No solution found !')

            #Format solution data for frontend
            output = []
            for vehicle_id in range(vehicleNumber):
                trip = []
                index = routing.Start(vehicle_id)
                while not routing.IsEnd(index):
                    index = solution.Value(routing.NextVar(index))

                    #Exclude depot indices
                    if (index != 0 )& (int(index) < 51):
                        trip.append(Destination(index,parks_df["UNIT_NAME"][index-1],[parks_df["visitor_lon"][int(index)-1],parks_df["visitor_lat"][int(index)-1]],time_on_site = 0))
                output.append(trip)

            #print directions objects for debugging purposes
            for trip in output:
                for park in trip:
                    print(park.park_name)
                print("\n")

            #Generate google maps http request piece
            urls = []
            for trip in output:
                print(trip)
                url = f"&origin={self.homeAddress.replace(' ', '+')}&waypoints="
                for park in trip:
                    url += f"{park.coordinates[1]},{park.coordinates[0]}|"
                url = url.rstrip(url[-1])
                url += f"&destination={self.homeAddress.replace(' ', '+')}"
                urls.append(url)
            return output, urls

class Destination:
    def __init__(self, park_id,park_name, coordinates, time_on_site):
        self.park_id = park_id
        self.park_name = park_name
        self.coordinates = coordinates
        self.time_on_site = time_on_site





