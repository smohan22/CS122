
# The code below was used to construct our databases. I tried to preserve as much of it as possible.

#The code below was extracted from an IPython notebook.

# In[3]:

# import googlemaps
# import pandas as pd
# from uber_rides.session import Session
# from uber_rides.client import UberRidesClient
# import json
# import requests
# from bs4 import BeautifulSoup
# import urllib
# import json
# import ast

# ############# UBER API
# session = Session(server_token='INSERT TOKEN HERE')
# client = UberRidesClient(session)

# ############ GOOGLE API
# # gmaps = googlemaps.Client(key='API KEY', timeout=None)

# gmaps = googlemaps.Client(key="API KEY", timeout=None)


# In[2]:

# CPS_data_table = pd.read_csv('CPS College Attendance Data copy.csv')
# CPS_data_clean = CPS_data_table.dropna()
# CPS_data = CPS_data_clean.copy(deep=True)
# CPS_data=CPS_data.rename(columns = {'new_name':'Comp_Level'})


# In[3]:

# list_of_all_college_names = []
# for i in CPS_data['Name of College']:
#     list_of_all_college_names.append(i)


# In[430]:

# list_of_all_zip_codes = []

# for i in list(CPS_data["Name of College"]):
#     geocode_result = gmaps.geocode(i)
#     print(i)
#     print()
#     geocode_result_1 = geocode_result[0]['address_components'][-1]
#     print(geocode_result_1)
#     print()
#     geocode_result_2 = geocode_result[0]['address_components'][-2]
#     print(geocode_result_2)
#     print()
    
#     if geocode_result_1['types'] == ['postal_code']:
#         list_of_all_zip_codes.append(geocode_result_1['short_name'])
#     else:
#         list_of_all_zip_codes.append(geocode_result_2['short_name'])
# #     list_of_all_zip_codes.append(geocode_result[0]['address_components'][-1]['short_name'])
# CPS_data["Zip Code"] = list_of_all_zip_codes


# In[5]:

# list_of_all_lats = []
# list_of_all_lon = []

# for i in list_of_all_college_names:
#     geocode_result_coords = gmaps.geocode(i)
#     list_of_all_lats.append([geocode_result_coords[0]['geometry']['location']['lat']])
#     list_of_all_lon.append([geocode_result_coords[0]['geometry']['location']['lng']])


# In[6]:

# list_of_latitude = sum(list_of_all_lats, [])
# list_of_longitude = sum(list_of_all_lon, [])


# In[7]:

# list_of_all_states = []

# for i in list_of_all_college_names:
#     geocode_result_states = gmaps.geocode(i)
#     address_info = geocode_result_states[0]['address_components']
#     for info in address_info:
#         if len(info['short_name']) == 2 and info['short_name'] != 'US':
#             if info['short_name'] != '30':
#                 list_of_all_states.append(info['short_name'])


# In[8]:

# CPS_data['Latitude'] =  list_of_latitude
# CPS_data['Longitude'] = list_of_longitude
# CPS_data['State'] = list_of_all_states


# In[433]:

# list_of_citys_dictionary = []
# for zipc in list(CPS_data['Zip Code']):
#     geocode_result = gmaps.geocode(str(zipc))
#     list_of_citys_dictionary.append(geocode_result[0]['address_components'])


# In[581]:

# #used a set to prevent duplicated from occuring. Google api is a little messy
# list_of_citys = []
# s = set()
# s.add((6, 2))
# s.add((10, 2))
# s.add((14, 2))
# s.add((21, 2))
# s.add((28, 2))
# s.add((30, 2))
# s.add((64, 2))
# for i in range(len(list_of_citys_dictionary)):
#     for j in range(len(list_of_citys_dictionary[i])):
#         if (i,j+1) not in s:
#             if list_of_citys_dictionary[i][j]['types'] == ['locality', 'political']:
#                 list_of_citys.append(list_of_citys_dictionary[i][j]['long_name'])
#             elif list_of_citys_dictionary[i][j]['types'] == ['neighborhood', 'political']:
#                 list_of_citys.append(list_of_citys_dictionary[i][j]['long_name'])


# In[582]:

# CPS_data['City'] = list_of_citys


# In[584]:

# CPS_data


# In[585]:

# CPS_data.to_csv("CPS_Final_Data_Pandas.csv", index=False)


# In[ ]:

# CPS_data = pd.read_csv("CPS_Final_Data_Pandas.csv")


# In[290]:




# **AIRPORT DATASET CONSTRUCTION BELOW**

# In[ ]:




# In[10]:

# airport_data = pd.read_excel('Airport_Data.xlsx', encoding = 'latin-1')

# airport_unclean_list = []

# for i in airport_data['Airport']:
#     airport_unclean_list.append(i)

# airport_clean_list = []
# for i in airport_unclean_list:
#     if u'\xa0' in i:
#         clean_it = i.replace(u'\xa0', u' ')
#         airport_clean_list.append(clean_it)
#     else:
#         airport_clean_list.append(i)


# In[11]:

# airport_lats = []
# airport_lon = []

# for i in airport_clean_list:
#     geocode_result_airport = gmaps.geocode(i)
#     airport_lats.append([geocode_result_airport[0]['geometry']['location']['lat']])
#     airport_lon.append([geocode_result_airport[0]['geometry']['location']['lng']])


# In[12]:

# list_of_airport_lats = sum(airport_lats, [])
# list_of_airport_lon = sum(airport_lon, [])
# airport_data['Latitude'] = list_of_airport_lats
# airport_data['Longitude'] = list_of_airport_lon
# airport_data


# In[15]:

# airport_data.to_csv("airport_data_final_pandas.csv", index=False)


# In[19]:

# airport_data = pd.read_csv("airport_data_final_pandas.csv")


# In[20]:

# airport_data


# In[570]:

# airport_data.loc[airport_data['Airport'] == "Chicago O'Hare International Airport"]
# airport_data[airport_data.State == 'IL']


# **UBER STUFF BELOW**

# In[250]:

# def uber_to_ORD(address):
#     '''
#     This function will return the estimated price, distance (in miles) and duration (in minutes) of a journey 
#     from an individuals starting address to the Chicago 0'Hare Airport
#     '''
#     geocode_result = gmaps.geocode(address)
#     a_start = geocode_result[0]['geometry']['location']['lat']
#     a_end = geocode_result[0]['geometry']['location']['lng']
    
#     geocode_result2 = gmaps.geocode('ORD')
#     b_start = geocode_result2[0]['geometry']['location']['lat']
#     b_end = geocode_result2[0]['geometry']['location']['lng']
    
#     response = client.get_price_estimates(
#     start_latitude = a_start,
#     start_longitude = a_end,
#     end_latitude = b_start,
#     end_longitude = b_end,
#     seat_count = 1
#     )
    
#     uber_query = response.json.get('prices')
    
#     g_distance = gmaps.distance_matrix((a_start,
#                                         a_end),
#                                        (b_start, b_end),
#                                        mode = "driving", 
#                                        units ="imperial")
    
#     distance = g_distance['rows'][0]['elements'][0]['distance']['text']
#     cost = uber_query[1]['estimate']
#     duration = (uber_query[1]['duration'])/60
    
#     return """The estimated distance to Chicago O'Hare Intl is %s. This trip will take approx. %d mins and cost %s"""%(
#     distance,duration, cost)


# In[6]:

# geocode_result = gmaps.geocode("UNIVERSITY OF WISCONSIN - MADISON ")
# a_start = geocode_result[0]['geometry']['location']['lat']
# a_end = geocode_result[0]['geometry']['location']['lng']
# print(a_start)
# print(a_end)


# In[7]:

# database = pd.read_csv("CPS_Final_Data_Pandas.csv")


# In[12]:

# database


# In[79]:

# city = list(database[database["Latitude"] == 42.2780436]['City'])[0]


# In[15]:

# database[database["Latitude"] == 43.076592]


# In[80]:

# city


# In[ ]:

# (43.076592, -89.4124875)


# In[5]:

# database[database["Latitude"] == 41.79636989999999]


# In[54]:

# database


# In[50]:

# o = list(test["City"])
# p = list(test["State"])

# list1 = list(zip(o,p))
# dict(list1)


# In[ ]:




# In[251]:

# uber_to_ORD("79 N Michigan Ave, Chicago, IL")


# In[424]:

# air_dict = {"JP": "Adria Airways",
# "A3": "Aegean Airlines",
# "RE": "Aer Arann",
# "EI": "Aer Lingus",
# "SU": "Aeroflot Russian Airlines",
# "AR": "Aerolineas Argentinas",
# "AM": "Aeromexico",
# "AH": "Air Algerie",
# "KC": "Air Astana",
# "AB": "Air Berlin",
# "AC": "Air Canada",
# "CA": "Air China",
# "UX": "Air Europa",
# "AF": "Air France",
# "AI": "Air India",
# "KM": "Air Malta",
# "SW": "Air Namibia",
# "NZ": "Air New Zealand",
# "HM": "Air Seychelles",
# "VT": "Air Tahiti",
# "UM": "Air Zimbabwe",
# "AS": "Alaska Airlines",
# "AZ": "Alitalia",
# "NH": "All Nippon Airways",
# "AA": "American Airlines",
# "W3": "Arik Air",
# "OZ": "Asiana Airlines",
# "RC": "Atlantic Airways",
# "GR": "Aurigny",
# "OS": "Austrian Airlines",
# "AV": "Avianca",
# "J2": "Azerbaijan Hava Yollary",
# "PG": "Bangkok Airways",
# "KF": "Blue1",
# "BA": "British Airways",
# "SN": "Brussels Airlines",
# "FB": "Bulgaria Air",
# "CX": "Cathay Pacific",
# "OK": "Czech Airlines",
# "CI": "China Airlines",
# "MU": "China Eastern Airlines",
# "CZ": "China Southern Airlines",
# "OU": "Croatia Airlines",
# "CY": "Cyprus Airways",
# "DL": "Delta Air Lines",
# "T3": "Eastern Airways",
# "MS": "Egyptair",
# "LY": "El Al Israel Airlines",
# "EK": "Emirates",
# "OV": "Estonian Air",
# "ET": "Ethiopian Airlines",
# "EY": "Etihad Airways",
# "BR": "Eva Air",
# "AY": "Finnair",
# "BE": "Flybe",
# "GA": "Garuda Indonesia",
# "GF": "Gulf Air",
# "HR": "HAHN Air",
# "HX": "Hong Kong Airlines",
# "IB": "Iberia",
# "FI": "Icelandair",
# "JL": "Japan Airlines",
# "9W": "Jet Airways",
# "KQ": "Kenya Airways",
# "KL": "KLM Royal Dutch Airlines",
# "KE": "Korean Air",
# "KU": "Kuwait Airways",
# "LA": "LAN Colombia",
# "LO": "LOT - Polish Airlines",
# "LH": "Lufthansa",
# "LG": "Luxair",
# "MH": "Malaysia Airlines",
# "ME": "Middle East Airlines",
# "IG": "Meridiana",
# "MX": "Mexicana",
# "ZB": "Monarch Airlines",
# "NW": "Northwest Airlines",
# "DY": "Norwegian Air Shuttle",
# "OA": "Olympic Air",
# "WY": "Oman Air",
# "FV": "Rossiya-Russia Airlines",
# "QF": "Qantas Airways",
# "QR": "Qatar Airways",
# "AT": "Royal Air Maroc",
# "BI": "Royal Brunei Airlines",
# "RJ": "Royal Jordanian",
# "S7": "Siberia Airlines",
# "SV": "Saudi Arabian Airlines",
# "SK": "Scandinavian Airlines System (SAS)",
# "SQ": "Singapore Airlines",
# "SA": "South African Airways",
# "JK": "Spanair",
# "UL": "SriLankan Airlines",
# "LX": "SWISS International Air Lines",
# "JJ": "TAM Airlines",
# "TP": "TAP Portugal",
# "RO": "Tarom",
# "TG": "Thai Airways International",
# "UN": "Transaero Airlines",
# "TU": "Tunisair",
# "TK": "Turkish Airlines",
# "PS": "Ukraine International Airlines",
# "UA": "United Airlines",
# "US": "US Airways",
# "HY": "Uzbekistan Airways",
# "VN": "Vietnam Airlines",
# "VS": "Virgin Atlantic Airways",
# "VG": "VLM Airlines (Cityjet)"}


# ### FLIGHT STUFF BELOW

# In[425]:

# def find_flights(origin, destination, passengers, From, To):
#     url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=AIzaSyBJN3O55GnOaHOo85FKvUsZQ-Jxq5piO7g"
#     headers = {'content-type': 'application/json'}

#     params = {
#       "request": {
#         "slice": [{"origin": origin,"destination": destination,"date": From, "maxStops": 0},
#                   {"origin": destination, "destination": origin, "date": To, "maxStops": 0}
#         ],
#         "passengers": {
#           "adultCount": passengers
#         },
#         "solutions": 5, # only return top 5 cheapest search results.
#         "refundable": "false"
#       }
#     }

#     response = requests.post(url, data=json.dumps(params), headers=headers)
#     data = response.json()
    
#     for i in range(len(data['trips']['tripOption'])):

#         base = data['trips']['tripOption'][i]

#         #cost
#         cost = base['saleTotal'][:3] + " " + base['saleTotal'][3:]

#         #Go to
#         #flight info 
#         to_depart_ap = base['slice'][0]['segment'][0]["leg"][0]["origin"]
#         to_arrive_ap = base['slice'][0]['segment'][0]["leg"][0]["destination"]
#         to_duration = base['slice'][0]['segment'][0]['duration']
#         to_depart = base['slice'][0]['segment'][0]["leg"][0]["departureTime"]
#         to_arrive = base['slice'][0]['segment'][0]["leg"][0]["arrivalTime"]

#         #flight number
#         to_carrier = base['slice'][0]['segment'][0]["flight"]["carrier"]
#         to_flnumber = base['slice'][0]['segment'][0]["flight"]["number"]


#         #Come back
#         #flight info
#         back_depart_ap = base['slice'][1]['segment'][0]["leg"][0]["origin"]
#         back_arrive_ap = base['slice'][1]['segment'][0]["leg"][0]["destination"]
#         back_duration = base['slice'][1]['segment'][0]['duration']
#         back_depart = base['slice'][1]['segment'][0]["leg"][0]["departureTime"]
#         back_arrive = base['slice'][1]['segment'][0]["leg"][0]["arrivalTime"]

#         #flight number
#         back_carrier = base['slice'][1]['segment'][0]["flight"]["carrier"]
#         back_flnumber = base['slice'][1]['segment'][0]["flight"]["number"]
        

#         #Cleaning the strings
#         to_depart = to_depart[0:10] + " " + to_depart[11:16] 
#         to_arrive = to_arrive[0:10] + " " + to_arrive[11:16]
#         to_duration = str(to_duration//60) + " h " + str(to_duration%60) + " min"
#         to_carrier = air_dict[to_carrier]

#         back_depart = back_depart[0:10] + " " + back_depart[11:16] 
#         back_arrive = back_arrive[0:10] + " " + back_arrive[11:16]
#         back_duration = str(back_duration//60) + " h " + str(back_duration%60) + " min"
#         back_carrier = air_dict[back_carrier]


# #         print(cost,to_depart_ap,to_depart,to_arrive_ap,to_arrive,to_duration,to_carrier,to_flnumber,back_depart_ap,back_depart,back_arrive_ap,back_arrive,back_duration,back_duration,back_carrier,back_flnumber)
        
        
#         print("-------------- Flight Option:",i+1, "--------------")
#         print()

#         print("Total Cost of Journey: ", cost)
#         print()

#         print("-------------- First Leg --------------------")
#         print()

#         print("Flight: ", to_carrier, to_flnumber)
#         print("Origin: ", to_depart_ap)
#         print("Destination: ", to_arrive_ap)
#         print("Duration: ", to_duration)
#         print("Departure Time: ", to_depart)
#         print("Arrival Time: ", to_arrive)
#         print()

#         print("-------------- Second Leg --------------------")
#         print()

#         print("Flight: ", back_carrier, back_flnumber)
#         print("Origin: ", back_depart_ap)
#         print("Destination: ", back_arrive_ap)
#         print("Duration: ", back_duration)
#         print("Departure Time: ", back_depart)
#         print("Arrival Time: ", back_arrive)
#         print()
        
        


# In[429]:

# find_flights("ORD", "PHL",1,"2017-03-15","2017-03-20")


# In[297]:

# def url_1(abbr):
#     multi_word = abbr.split()
#     if len(multi_word) == 2:
#         return "https://pegasus.greyhound.com/GhWebsite/locations/locationsStation?name="+v[0]+"%20"+v[1]+"&type=Origin"
#     else:
#         return "https://pegasus.greyhound.com/GhWebsite/locations/locationsStation?name=%s&type=Origin"%abbr


# In[296]:

# url_1("New York")


# In[300]:

# def url1_to_dict(url):
#     address = url
#     pm = urllib3.PoolManager()
#     html = pm.urlopen(url=address, method='GET').data
#     soup = bs4.BeautifulSoup(html, 'lxml')
#     data = soup.text
#     data_clean = data.replace("false", '"hello"')
#     return ast.literal_eval(data_clean)

# # y_u[200:205]

# # v = y_u.replace("false", '"hello"')
# # f = ast.literal_eval(v)
# # f






# In[301]:

# url1_to_dict('https://pegasus.greyhound.com/GhWebsite/locations/locationsStation?name=New%20York&type=Origin')


# In[ ]:




# In[ ]:




# In[ ]:




# In[17]:

# # from datetime import datetime

# master_list_of_colleges = []

# gmaps = googlemaps.Client(key='AIzaSyAukdu1BlNyNgreb97Mv26rbQmT6awNjaE')

# # Geocoding an address
# geocode_result2 = gmaps.geocode('1330 E 53rd St, Chicago, IL')

# geocode_result2

# # Look up an address with reverse geocoding
# # reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# # # Request directions via public transit
# # now = datetime.now()
# # directions_result = gmaps.directions("Sydney Town Hall",
# #                                      "Parramatta, NSW",
# #                                      mode="transit",
# #                                      departure_time=now)



# In[ ]:

# g = geocode_result2[0]['address_components']
# g
# list_empty = []
# for i in g:
#     if len(i['short_name']) == 2 and i['short_name'] != 'US':
#         list_empty.append(i['short_name'])
# list_empty


# In[232]:

# response = client.get_price_estimates(
#     start_latitude = 41.974162,
#     start_longitude = -87.907321,
#     end_latitude = 41.7998074,
#     end_longitude = -87.5937119,
#     seat_count = 1
# )
    
# result74 = response.json.get('prices')
    
# result74[1]

# #ORD TO MY PLACE


# In[230]:

# response = client.get_price_estimates(
#     start_latitude = 41.7998074,
#     start_longitude = -87.5937119,
#     end_latitude = 41.974162,
#     end_longitude = -87.907321,
#     seat_count = 1
# )
    
# result1 = response.json.get('prices')
    
# result1[1]

# #MY HOUSE TO ORD


# In[455]:

# test1 = gmaps.distance_matrix((41.7980372,-87.5924325),(41.974162, -87.907321), mode="transit", units="imperial")
# # test1.keys()


# In[231]:

# test1


# In[467]:

# test2 = gmaps.geocode("ORD")


# In[229]:

# test2[0]['geometry']['location']


# In[227]:

# def find_flights(origin, destination, passengers, From, To):
#     url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=AIzaSyBJN3O55GnOaHOo85FKvUsZQ-Jxq5piO7g"
#     headers = {'content-type': 'application/json'}

#     params = {
#       "request": {
#         "slice": [{"origin": origin,"destination": destination,"date": From, "maxStops": 0},
#                   {"origin": destination, "destination": origin, "date": To, "maxStops": 0}
#         ],
#         "passengers": {
#           "adultCount": passengers
#         },
#         "solutions": 5,
#         "refundable": "false"
#       }
#     }

#     response = requests.post(url, data=json.dumps(params), headers=headers)
#     data = response.json()
    
#     for i in range(len(data['trips']['tripOption'])):

#         base = data['trips']['tripOption'][i]

#         #cost
#         cost = base['saleTotal']

#         #Go to
#         #flight info 
#         to_depart_ap = base['slice'][0]['segment'][0]["leg"][0]["origin"]
#         to_arrive_ap = base['slice'][0]['segment'][0]["leg"][0]["destination"]
#         to_duration = base['slice'][0]['segment'][0]['duration']
#         to_depart = base['slice'][0]['segment'][0]["leg"][0]["departureTime"]
#         to_arrive = base['slice'][0]['segment'][0]["leg"][0]["arrivalTime"]

#         #flight number
#         to_carrier = base['slice'][0]['segment'][0]["flight"]["carrier"]
#         to_flnumber = base['slice'][0]['segment'][0]["flight"]["number"]


#         #t=data['trips']['tripOption'][0]['slice'][1]['segment'][0]["leg"][0]["departureTime"]
#         #Come back
#         #flight info
#         back_depart_ap = base['slice'][1]['segment'][0]["leg"][0]["origin"]
#         back_arrive_ap = base['slice'][1]['segment'][0]["leg"][0]["destination"]
#         back_duration = base['slice'][1]['segment'][0]['duration']
#         back_depart = base['slice'][1]['segment'][0]["leg"][0]["departureTime"]
#         back_arrive = base['slice'][1]['segment'][0]["leg"][0]["arrivalTime"]

#         #flight number
#         back_carrier = base['slice'][1]['segment'][0]["flight"]["carrier"]
#         back_flnumber = base['slice'][1]['segment'][0]["flight"]["number"]
        

#         to_depart = to_depart[0:10] + " " + to_depart[11:16] 
#         to_arrive = to_arrive[0:10] + " " + to_arrive[11:16]
#         to_duration = str(to_duration//60) + " h " + str(to_duration%60) + " min"
# #         to_carrier = air_dict[to_carrier]

#         back_depart = back_depart[0:10] + " " + back_depart[11:16] 
#         back_arrive = back_arrive[0:10] + " " + back_arrive[11:16]
#         back_duration = str(back_duration//60) + " h " + str(back_duration%60) + " min"
# #         back_carrier = air_dict[back_carrier]


#         print(cost,to_depart_ap,to_depart,to_arrive_ap,to_arrive,to_duration,to_flnumber,back_depart_ap,back_depart,back_arrive_ap,back_arrive,back_duration,back_flnumber)


# In[228]:

# find_flights("ORD", "PHL", 1,"2017-03-17","2017-03-24")


# data['trips']['tripOption'][0] <-- this will go from 0 to 4 for the top 5 flights (they will already be sorted as the cheapest)
# 
# then
# 
# data['trips']['tripOption'][0]['saleTotal'] --> the total price for the 0th flight (incl. first and second leg)
# 
# data['trips']['tripOption'][0]['slice'][0] --> first leg
# data['trips']['tripOption'][0]['slice'][0]['segment'][0]['duration'] --> duration in mins for first leg
# data['trips']['tripOption'][0]['slice'][0]['segment'][0]['flight']['carrier'] --> carrier name for first leg
# data['trips']['tripOption'][0]['slice'][0]['segment'][0]['flight']['number'] --> flight number for first leg
# data['trips']['tripOption'][0]['slice'][0]['segment'][0]['leg'][0]['arrivalTime'] --> arrival time at destination
# data['trips']['tripOption'][0]['slice'][0]['segment'][0]['leg'][0]['departureTime'] --> departure time at origin
# data['trips']['tripOption'][0]['slice'][0]['segment'][0]['leg'][0]['origin] --> location of origin airport
# data['trips']['tripOption'][0]['slice'][0]['segment'][0]['leg'][0]['destination'] --> location of destination airport
# 
# data['trips']['tripOption'][0]['slice'][1] --> second leg
# data['trips']['tripOption'][0]['slice'][1]['segment'][0]['duration'] --> duration in mins for second leg
# data['trips']['tripOption'][0]['slice'][1]['segment'][0]['flight']['carrier'] --> carrier name for second leg
# data['trips']['tripOption'][0]['slice'][1]['segment'][0]['flight']['number'] --> flight number for second leg
# data['trips']['tripOption'][0]['slice'][1]['segment'][0]['leg'][0]['arrivalTime'] --> arrival time at destination
# data['trips']['tripOption'][0]['slice'][1]['segment'][0]['leg'][0]['departureTime'] --> departure time at origin
# data['trips']['tripOption'][0]['slice'][1]['segment'][0]['leg'][0]['origin] --> location of origin airport
# data['trips']['tripOption'][0]['slice'][1]['segment'][0]['leg'][0]['destination'] --> location of destination airport

# In[224]:

# data['trips']['tripOption'][0]['saleTotal']


# In[225]:

# flight_cost

# for i,val in enumerate(range(20)):
#     print(data['trips']['tripOption'][i]['saleTotal'], i)


# In[226]:

# params = {
#   "request": {
#     "passengers": {
#       "kind": "qpxexpress#passengerCounts",
#       "adultCount": integer,
#       "childCount": integer,
#       "infantInLapCount": integer,
#       "infantInSeatCount": integer,
#       "seniorCount": integer
#     },
#     "slice": [
#       {
#         "kind": "qpxexpress#sliceInput",
#         "origin": string,
#         "destination": string,
#         "date": string,
#         "maxStops": integer,
#         "maxConnectionDuration": integer,
#         "preferredCabin": string,
#         "permittedDepartureTime": {
#           "kind": "qpxexpress#timeOfDayRange",
#           "earliestTime": string,
#           "latestTime": string
#         },
#         "permittedCarrier": [
#           string
#         ],
#         "alliance": string,
#         "prohibitedCarrier": [
#           string
#         ]
#       }
#     ],
#     "maxPrice": string,
#     "saleCountry": string,
#     "ticketingCountry": string,
#     "refundable": boolean,
#     "solutions": integer
#   }
# }


# In[ ]:

# option code
# import json
# import requests

# # api_key = "AIzaSyAukdu1BlNyNgreb97Mv26rbQmT6awNjaE"
# url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=AIzaSyBJN3O55GnOaHOo85FKvUsZQ-Jxq5piO7g"
# headers = {'content-type': 'application/json'}

# params = {
#   "request": {
#     "slice": [{"origin": "ORD","destination": "PHL","date": "2017-03-17", "maxStops": 0},
#               {"origin": "PHL", "destination": "ORD", "date": "2017-03-24", "maxStops": 0}
#     ],
#     "passengers": {
#       "adultCount": 1
#     },
#     "solutions": 20,
#     "refundable": "false"
#   }
# }

# response = requests.post(url, data=json.dumps(params), headers=headers)
# data = response.json()
# # json.loads(response.data.decode('utf-8'))


# In[15]:

# def hotel_price_dict(file):
    
#     df = pd.read_csv(file)
#     price_dict = {}
    
#     for i in range(len(df.index)):
#         city = df.iloc[i,0].strip()
#         if city in price_dict:
#             price_dict[city][df.iloc[i, 1]] = df.iloc[i, 2]
#         else:
#             price_dict[city] = {df.iloc[i, 1]: df.iloc[i, 2]}
#     return price_dict


# In[16]:

# hotel_price_dict("Hotel_Prices.csv")


# In[12]:

# hotel_prices = {'Allendale': {'$': 50, '$$': 100, '$$$': 150},
#  'Ames': {'$': 60, '$$': 125, '$$$': 150},
#  'Ann Arbor': {'$': 70, '$$': 160, '$$$': 179},
#  'Atlanta': {'$': 50, '$$': 200, '$$$': 450},
#  'Aurora': {'$': 110, '$$': 120, '$$$': 150},
#  'Beloit': {'$': 70, '$$': 150, '$$$': 150},
#  'Bloomington': {'$': 69, '$$': 130, '$$$': 150},
#  'Cambridge': {'$': 50, '$$': 200, '$$$': 400},
#  'Carbondale': {'$': 56, '$$': 110, '$$$': 199},
#  'Carlinville': {'$': 50, '$$': 100, '$$$': 150},
#  'Cedar Rapids': {'$': 65, '$$': 130, '$$$': 160},
#  'Champaign': {'$': 59, '$$': 120, '$$$': 130},
#  'Charleston': {'$': 50, '$$': 100, '$$$': 150},
#  'Chicago': {'$': 50, '$$': 206, '$$$': 385},
#  'Cicero': {'$': 60, '$$': 100, '$$$': 150},
#  'Columbia': {'$': 55, '$$': 180, '$$$': 159},
#  'Coraopolis': {'$': 63, '$$': 160, '$$$': 160},
#  'DeKalb': {'$': 62, '$$': 131, '$$$': 113},
#  'Decatur': {'$': 50, '$$': 86, '$$$': 100},
#  'Des Plaines': {'$': 100, '$$': 195, '$$$': 250},
#  'Downers Grove': {'$': 60, '$$': 220, '$$$': 230},
#  'Dubuque': {'$': 85, '$$': 120, '$$$': 170},
#  'East Lansing': {'$': 50, '$$': 150, '$$$': 200},
#  'Edwardsville': {'$': 62, '$$': 117, '$$$': 129},
#  'Elmhurst': {'$': 50, '$$': 100, '$$$': 150},
#  'Evanston': {'$': 50, '$$': 221, '$$$': 230},
#  'Fairfield': {'$': 50, '$$': 100, '$$$': 150},
#  'Fayette': {'$': 40, '$$': 90, '$$$': 100},
#  'Galesburg': {'$': 59, '$$': 140, '$$$': 175},
#  'Glen Ellyn': {'$': 50, '$$': 120, '$$$': 120},
#  'Graham': {'$': 50, '$$': 100, '$$$': 150},
#  'Granville': {'$': 50, '$$': 100, '$$$': 150},
#  'Greencastle': {'$': 60, '$$': 100, '$$$': 150},
#  'Holland': {'$': 70, '$$': 170, '$$$': 200},
#  'Huntstville': {'$': 100, '$$': 260, '$$$': 250},
#  'Iowa City': {'$': 56, '$$': 150, '$$$': 175},
#  'Ithaca': {'$': 110, '$$': 180, '$$$': 200},
#  'Jackson': {'$': 60, '$$': 150, '$$$': 110},
#  'Jacksonville': {'$': 65, '$$': 80, '$$$': 180},
#  'Joliet': {'$': 59, '$$': 89, '$$$': 120},
#  'Kenosha': {'$': 50, '$$': 100, '$$$': 150},
#  'Lake Forest': {'$': 50, '$$': 100, '$$$': 150},
#  'Lexington': {'$': 67, '$$': 154, '$$$': 300},
#  'Lincoln': {'$': 50, '$$': 125, '$$$': 150},
#  'Lincoln University': {'$': 50, '$$': 100, '$$$': 150},
#  'Little Rock': {'$': 56, '$$': 155, '$$$': 195},
#  'Los Angeles': {'$': 120, '$$': 250, '$$$': 320},
#  'Macomb': {'$': 50, '$$': 111, '$$$': 130},
#  'Madison': {'$': 81, '$$': 185, '$$$': 216},
#  'Malta': {'$': 50, '$$': 100, '$$$': 150},
#  'Milwaukee': {'$': 75, '$$': 140, '$$$': 250},
#  'Monmouth': {'$': 50, '$$': 100, '$$$': 150},
#  'Montgomery': {'$': 50, '$$': 110, '$$$': 250},
#  'Mount Pleasant': {'$': 100, '$$': 150, '$$$': 175},
#  'Muncie': {'$': 70, '$$': 150, '$$$': 175},
#  'Nashville': {'$': 50, '$$': 250, '$$$': 350},
#  'New York': {'$': 100, '$$': 269, '$$$': 350},
#  'Normal': {'$': 50, '$$': 136, '$$$': 140},
#  'Northfield': {'$': 50, '$$': 100, '$$$': 120},
#  'Oberlin': {'$': 100, '$$': 200, '$$$': 250},
#  'Palantine': {'$': 50, '$$': 100, '$$$': 150},
#  'Palos Hills': {'$': 50, '$$': 100, '$$$': 150},
#  'Peoria': {'$': 120, '$$': 140, '$$$': 160},
#  'Pine Bluff': {'$': 60, '$$': 150, '$$$': 150},
#  'Portland': {'$': 50, '$$': 120, '$$$': 190},
#  'Quincy': {'$': 50, '$$': 100, '$$$': 150},
#  'River Forest': {'$': 50, '$$': 100, '$$$': 130},
#  'Romeoville': {'$': 50, '$$': 110, '$$$': 150},
#  'South Holland': {'$': 50, '$$': 100, '$$$': 150},
#  'Springfield': {'$': 59, '$$': 100, '$$$': 130},
#  'St. Louis': {'$': 140, '$$': 180, '$$$': 350},
#  'Terre Haute': {'$': 50, '$$': 100, '$$$': 150},
#  'Tougaloo': {'$': 50, '$$': 100, '$$$': 150},
#  'Tuskegee': {'$': 89, '$$': 120, '$$$': 150},
#  'University Park': {'$': 50, '$$': 100, '$$$': 150},
#  'Urbana': {'$': 54, '$$': 118, '$$$': 169},
#  'Valparaiso': {'$': 65, '$$': 150, '$$$': 150},
#  'Vincennes': {'$': 50, '$$': 110, '$$$': 130},
#  'Wilberforce': {'$': 50, '$$': 100, '$$$': 150}}


# In[17]:

# hotel_prices


# In[3]:

# test = pd.read_csv("CPS_Final_Data_Pandas.csv")


# In[8]:

# test


# In[34]:

# v = test[test["Name of College"] == "UNIVERSITY OF ILLINOIS @ URBANA "]


# In[37]:

# v.iloc[0]['City']


# In[29]:

# v['City'][0]


# In[38]:

# s = "$8-10"


# In[40]:

# s.split("-")[0][1:]



