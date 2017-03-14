import googlemaps
import pandas as pd
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
import json
import requests
from bs4 import BeautifulSoup
import urllib
import json
import ast
#make sure you install the approriate library (uber, google etc) on the VM for the demo.

############# UBER API
session = Session(server_token='API KEY') #UBER KEY
client = UberRidesClient(session)

############ GOOGLE API
gmaps = googlemaps.Client(key='API KEY') #GOOGLE KEY

################################################################################################################

def uber_to_ORD(address):
    '''
    This function will return the estimated price, distance (in miles) and duration (in minutes) of a journey 
    from an individuals starting address to the Chicago 0'Hare Airport

    Parameters
    -Address:
    	String
    Return
    	String containing price information.
    '''
    geocode_result = gmaps.geocode(address)
    a_start = geocode_result[0]['geometry']['location']['lat']
    a_end = geocode_result[0]['geometry']['location']['lng']
    
    geocode_result2 = gmaps.geocode('ORD')
    b_start = geocode_result2[0]['geometry']['location']['lat']
    b_end = geocode_result2[0]['geometry']['location']['lng']
    
    response = client.get_price_estimates(
    start_latitude = a_start,
    start_longitude = a_end,
    end_latitude = b_start,
    end_longitude = b_end,
    seat_count = 1
    )
    
    uber_query = response.json.get('prices')
    
    g_distance = gmaps.distance_matrix((a_start,
                                        a_end),
                                       (b_start, b_end),
                                       mode = "driving", 
                                       units ="imperial")
    
    distance = g_distance['rows'][0]['elements'][0]['distance']['text']
    cost = uber_query[1]['estimate']
    duration = (uber_query[1]['duration'])/60
    
    return """The estimated distance to Chicago O'Hare Intl is %s. This trip will take approx. %d mins and cost %s"""%(
    distance,duration, cost)
################################################### SAMPLE USE OF FUNCTION ###################################################

#uber_to_ORD("79 N Michigan Ave, Chicago, IL") - THIS HAS BEEN HASHED OUT - TYPE INTO PYTHON CONSOLE

####THIS IS THE AIRDICT REQUIRED FOR THE PRICING ALOGRITHM.

air_dict = {"JP": "Adria Airways",
"A3": "Aegean Airlines",
"RE": "Aer Arann",
"EI": "Aer Lingus",
"SU": "Aeroflot Russian Airlines",
"AR": "Aerolineas Argentinas",
"AM": "Aeromexico",
"AH": "Air Algerie",
"KC": "Air Astana",
"AB": "Air Berlin",
"AC": "Air Canada",
"CA": "Air China",
"UX": "Air Europa",
"AF": "Air France",
"AI": "Air India",
"KM": "Air Malta",
"SW": "Air Namibia",
"NZ": "Air New Zealand",
"HM": "Air Seychelles",
"VT": "Air Tahiti",
"UM": "Air Zimbabwe",
"AS": "Alaska Airlines",
"AZ": "Alitalia",
"NH": "All Nippon Airways",
"AA": "American Airlines",
"W3": "Arik Air",
"OZ": "Asiana Airlines",
"RC": "Atlantic Airways",
"GR": "Aurigny",
"OS": "Austrian Airlines",
"AV": "Avianca",
"J2": "Azerbaijan Hava Yollary",
"PG": "Bangkok Airways",
"KF": "Blue1",
"BA": "British Airways",
"SN": "Brussels Airlines",
"FB": "Bulgaria Air",
"CX": "Cathay Pacific",
"OK": "Czech Airlines",
"CI": "China Airlines",
"MU": "China Eastern Airlines",
"CZ": "China Southern Airlines",
"OU": "Croatia Airlines",
"CY": "Cyprus Airways",
"DL": "Delta Air Lines",
"T3": "Eastern Airways",
"MS": "Egyptair",
"LY": "El Al Israel Airlines",
"EK": "Emirates",
"OV": "Estonian Air",
"ET": "Ethiopian Airlines",
"EY": "Etihad Airways",
"BR": "Eva Air",
"AY": "Finnair",
"BE": "Flybe",
"GA": "Garuda Indonesia",
"GF": "Gulf Air",
"HR": "HAHN Air",
"HX": "Hong Kong Airlines",
"IB": "Iberia",
"FI": "Icelandair",
"JL": "Japan Airlines",
"9W": "Jet Airways",
"KQ": "Kenya Airways",
"KL": "KLM Royal Dutch Airlines",
"KE": "Korean Air",
"KU": "Kuwait Airways",
"LA": "LAN Colombia",
"LO": "LOT - Polish Airlines",
"LH": "Lufthansa",
"LG": "Luxair",
"MH": "Malaysia Airlines",
"ME": "Middle East Airlines",
"IG": "Meridiana",
"MX": "Mexicana",
"ZB": "Monarch Airlines",
"NW": "Northwest Airlines",
"DY": "Norwegian Air Shuttle",
"OA": "Olympic Air",
"WY": "Oman Air",
"FV": "Rossiya-Russia Airlines",
"QF": "Qantas Airways",
"QR": "Qatar Airways",
"AT": "Royal Air Maroc",
"BI": "Royal Brunei Airlines",
"RJ": "Royal Jordanian",
"S7": "Siberia Airlines",
"SV": "Saudi Arabian Airlines",
"SK": "Scandinavian Airlines System (SAS)",
"SQ": "Singapore Airlines",
"SA": "South African Airways",
"JK": "Spanair",
"UL": "SriLankan Airlines",
"LX": "SWISS International Air Lines",
"JJ": "TAM Airlines",
"TP": "TAP Portugal",
"RO": "Tarom",
"TG": "Thai Airways International",
"UN": "Transaero Airlines",
"TU": "Tunisair",
"TK": "Turkish Airlines",
"PS": "Ukraine International Airlines",
"UA": "United Airlines",
"US": "US Airways",
"HY": "Uzbekistan Airways",
"VN": "Vietnam Airlines",
"VS": "Virgin Atlantic Airways",
"VG": "VLM Airlines (Cityjet)"}


################################# HERE IS THE PRICING ALGORITHM ################ WITH THANKS TO SUNJOO FOR BEING AWESOME

def find_flights(origin, destination, passengers, From, To):
    url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=AIzaSyBJN3O55GnOaHOo85FKvUsZQ-Jxq5piO7g"
    headers = {'content-type': 'application/json'}

    params = {
      "request": {
        "slice": [{"origin": origin,"destination": destination,"date": From, "maxStops": 0},
                  {"origin": destination, "destination": origin, "date": To, "maxStops": 0}
        ],
        "passengers": {
          "adultCount": passengers
        },
        "solutions": 5, # only return top 5 cheapest search results.
        "refundable": "false"
      }
    }

    response = requests.post(url, data=json.dumps(params), headers=headers)
    data = response.json()
    
    for i in range(len(data['trips']['tripOption'])):

        base = data['trips']['tripOption'][i]

        #cost
        cost = base['saleTotal'][:3] + " " + base['saleTotal'][3:]

        #Go to
        #flight info 
        to_depart_ap = base['slice'][0]['segment'][0]["leg"][0]["origin"]
        to_arrive_ap = base['slice'][0]['segment'][0]["leg"][0]["destination"]
        to_duration = base['slice'][0]['segment'][0]['duration']
        to_depart = base['slice'][0]['segment'][0]["leg"][0]["departureTime"]
        to_arrive = base['slice'][0]['segment'][0]["leg"][0]["arrivalTime"]

        #flight number
        to_carrier = base['slice'][0]['segment'][0]["flight"]["carrier"]
        to_flnumber = base['slice'][0]['segment'][0]["flight"]["number"]


        #Come back
        #flight info
        back_depart_ap = base['slice'][1]['segment'][0]["leg"][0]["origin"]
        back_arrive_ap = base['slice'][1]['segment'][0]["leg"][0]["destination"]
        back_duration = base['slice'][1]['segment'][0]['duration']
        back_depart = base['slice'][1]['segment'][0]["leg"][0]["departureTime"]
        back_arrive = base['slice'][1]['segment'][0]["leg"][0]["arrivalTime"]

        #flight number
        back_carrier = base['slice'][1]['segment'][0]["flight"]["carrier"]
        back_flnumber = base['slice'][1]['segment'][0]["flight"]["number"]
        

        #Cleaning the strings
        to_depart = to_depart[0:10] + " " + to_depart[11:16] 
        to_arrive = to_arrive[0:10] + " " + to_arrive[11:16]
        to_duration = str(to_duration//60) + " h " + str(to_duration%60) + " min"
        to_carrier = air_dict[to_carrier]

        back_depart = back_depart[0:10] + " " + back_depart[11:16] 
        back_arrive = back_arrive[0:10] + " " + back_arrive[11:16]
        back_duration = str(back_duration//60) + " h " + str(back_duration%60) + " min"
        back_carrier = air_dict[back_carrier]


#         print(cost,to_depart_ap,to_depart,to_arrive_ap,to_arrive,to_duration,to_carrier,to_flnumber,back_depart_ap,back_depart,back_arrive_ap,back_arrive,back_duration,back_duration,back_carrier,back_flnumber)
        
        
        print("-------------- Flight Option:",i+1, "--------------")
        print()

        print("Total Cost of Journey: ", cost)
        print()

        print("-------------- First Leg --------------------")
        print()

        print("Flight: ", to_carrier, to_flnumber)
        print("Origin: ", to_depart_ap)
        print("Destination: ", to_arrive_ap)
        print("Duration: ", to_duration)
        print("Departure Time: ", to_depart)
        print("Arrival Time: ", to_arrive)
        print()

        print("-------------- Second Leg --------------------")
        print()

        print("Flight: ", back_carrier, back_flnumber)
        print("Origin: ", back_depart_ap)
        print("Destination: ", back_arrive_ap)
        print("Duration: ", back_duration)
        print("Departure Time: ", back_depart)
        print("Arrival Time: ", back_arrive)
        print()
        
###################################################### HERE IS THE SAMPLE USE OF THE FUNCTION########################

#find_flights("ORD", "PHL",1,"2017-03-17","2017-03-24") ------ THIS HAS BEEN HASHED OUT. TYPE INTO PYTHON TERMINAL

