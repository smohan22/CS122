import googlemaps
import pandas as pd
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
import json
import requests
from bs4 import BeautifulSoup
import urllib
import urllib3  #check if urllib3 includes all functions of urllib
import json
import ast
import requests
import time
import csv
import pandas as pd
from Yelp_Helper import *
from hotel_prices import *
 
############# UBER API
session = Session(server_token='vGZWQfF6e_h1n8khFs2uCN6XJCYmWb4dAEPnq0db') #UBER KEY
client = UberRidesClient(session)

############ GOOGLE API
gmaps = googlemaps.Client(key='AIzaSyAukdu1BlNyNgreb97Mv26rbQmT6awNjaE') #GOOGLE KEY


################################## DISTANCES ######################################
def get_lat_lng(address):
    '''
    Gets latitude and longitude of a given address.

    Input:
        address: string (ex: "79 N Michigan Ave, Chicago, IL", "ORD")
            or zip as integer (60615)
    Output:
        Tuple - containing the latitude and longitude of the given address

    address: string (ex: "79 N Michigan Ave, Chicago, IL", "ORD")
            or zip as integer (60615)
    '''
    geocode_result = gmaps.geocode(address)    
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
    return (lat, lng) 


def get_lat_lng_file(school): 
    '''
     Given the name of school, get the latitude and longitude.

    Input:
        String - school name

    Output:
        tuple of floats - containing the latitude and longitude


    '''
    cps_schools = pd.read_csv('CPS_Final_Data_Pandas.csv')

    sch_row = cps_schools['Name of College'] == school
    school_lat = cps_schools[sch_row]['Latitude']
    school_lng = cps_schools[sch_row]['Longitude']

    return (float(school_lat),float(school_lng))


def get_distance(a_lat, a_lng, b_lat, b_lng):
    '''
    Gets the distance between two locations, specified by their longitude and
    latitude.

    Inputs:
        a_lat - float, latitude of point A
        a_lng - float, longitude of point A
        b_lat - float, latitude of point B
        b_lng - float, longitude of point B

    Output:
        float - distance between the two locations


    '''
    g_distance = gmaps.distance_matrix((a_lat, a_lng),
                                       (b_lat, b_lng),
                                       mode = "driving", 
                                       units ="imperial")


    distance = g_distance['rows'][0]['elements'][0]['distance']['text']
    return distance


def get_city(school):
    '''
    Given the name of a school, finding its corresponding city.

    Input:
        string - name of school

    Output:
        string - name of city
    '''
    cps_schools = pd.read_csv('CPS_Final_Data_Pandas.csv')

    sch_row = cps_schools['Name of College'] == school
    city = cps_schools[sch_row].iloc[0]['City']
    return city


#################################### UBER #######################################
def uber_ride(from_lat, from_lng, to_lat, to_lng):
    '''
    This function will return the estimated price of a journey

    Parameters:
        from_lat - float, latitude of starting location
        from_lng - float, longitude of starting location
        to_lat - float, latitude of arrival location
        to_lng - float, longitude of arrival location

    Return:
        cost - float, coast of uber ride
    '''
        
    response = client.get_price_estimates(
    start_latitude = from_lat,
    start_longitude = from_lng,
    end_latitude = to_lat,
    end_longitude = to_lng
    )
    #print(response)
    uber_query = response.json.get('prices')
    #print("uber query", uber_query)
    cost = 0
    distance = get_distance(from_lat, from_lng, to_lat, to_lng)
    distance = float(distance[:-3])
    if len(uber_query) == 0:
        cost = 1.4+ distance*0.08
    else:
        if distance < 100:
            #print(uber_query[1], "UBER QUERY HERE!!")
            for each_dict in uber_query:
                for each_key in each_dict.keys():
                    if each_dict['localized_display_name'] == 'uberX':
                        cost = each_dict['low_estimate']
            #duration = (uber_query[0]['duration'])/60
        else:
            #estimated bus cost
            cost = int((9 + (0.08 * distance)) * num_people)
        
    return cost


################################# FLIGHT #######################################
def get_airport(school):
    '''
    Gets closest airport to a given school

    Input:
        school - string

    Output:
        closest_airport - string

    '''
    airports = pd.read_csv('airport_distance_final_pandas_database.csv')
    sch_row = airports['College'] == school 
    closest_airport = list(airports[sch_row]['Airport_Code'])[0]
    #print(closest_airport, "haha")
    return closest_airport


def find_flights(origin, destination1, departOn1, departOn2, num_people, destination2=None, departOn3=None):
    url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=AIzaSyBJN3O55GnOaHOo85FKvUsZQ-Jxq5piO7g"
    headers = {'content-type': 'application/json'}

    if destination2 == None:
        the_slice = [{"origin": origin,"destination": destination1,"date": departOn1, "maxStops": 1},
                  {"origin": destination1, "destination": origin, "date": departOn2, "maxStops": 1}]
    
    else:
        the_slice = [{"origin": origin,"destination": destination1,"date": departOn1, "maxStops": 1},
                  {"origin": destination1, "destination": destination2, "date": departOn2, "maxStops": 1},
                  {"origin": destination2, "destination": origin, "date": departOn3, "maxStops": 1}]
    params = {
      "request": {
        "slice": the_slice,
        "passengers": {
          "adultCount": num_people
        },
        "solutions": 5, 
        "refundable": "false"}}

    response = requests.post(url, data=json.dumps(params), headers=headers)
    data = response.json()
    flight_list = []
    
    if 'error' not in data:
        for i in range(len(data['trips']['tripOption'])):

            base = data['trips']['tripOption'][i]

            #cost
            cost = float(base['saleTotal'][3:])
            sub_list = []
            for j in range(len(base['slice'])):

                base2 = base['slice'][j]['segment'][0]
                
                #flight info 
                origin_ap = base2["leg"][0]["origin"]
                dest_ap = base2["leg"][0]["destination"]
                duration = base2["leg"][0]['duration']
                depart_time = base2["leg"][0]["departureTime"]
                arrive_time = base2["leg"][0]["arrivalTime"]

                #flight number
                carrier = base2["flight"]["carrier"]
                flnumber = base2["flight"]["number"]

                #Cleaning the strings
                depart_time = depart_time[0:10] + " " + depart_time[11:16] 
                arrive_time = arrive_time[0:10] + " " + arrive_time[11:16]
                duration = str(duration//60) + " h " + str(duration%60) + " min"
                carrier = air_dict[carrier]

                sub_tuple = (cost, origin_ap, depart_time, dest_ap, arrive_time, duration, carrier, flnumber)
                sub_list.append(sub_tuple)
            flight_list.append(sub_list)

    return flight_list

################################# BUS #########################################
#https://pegasus.greyhound.com/GhWebsite/locations/locationsState?name=chi&type=Destination&GPID=W201702222210002110
#details = 2, "2017-03-19", "2017-03-20",  'Chicago', 560252, 'IL', 56, 'New York', 151239, 'NY', 15

def url_1(abbr, loc_type):
    '''
    Returns the completed URL which is the first page to visit on the greyhound website.

    Inputs:
        abbr - string, name of the city (e.g. 'New York', 'Chicago')
        loc_type - string, location type ('destination' or 'arrival')
    '''

    multi_word = abbr.split()
    if len(multi_word) == 2:
        return "https://pegasus.greyhound.com/GhWebsite/locations/locationsStation?name="+multi_word[0]+"%20"+multi_word[1]+"&type=%s"%loc_type
    else:
        return "https://pegasus.greyhound.com/GhWebsite/locations/locationsStation?name=%(abbr)s&type=%(loc_type)s"%{"abbr": abbr, "loc_type": loc_type}


def url_to_dict(url):
    '''
    Function converts a url into a dictionary. Return dictionary is different depending on
    whether we send in URL1 or URL2. Returns details of the URL.
    '''
    address = url
    pm = urllib3.PoolManager()
    html = pm.urlopen(url=address, method='GET').data
    soup = BeautifulSoup(html, 'lxml')
    data = soup.text
    data_clean = data.replace("false", '"hello"')
    data_clean = data_clean.replace("true", '"hello"')
    return ast.literal_eval(data_clean) 


def extract_from_url1(location, loc_type):
    '''
    Extract the city, the code, the state abbreviation and the state code given the location
    and the location type.

    Inputs:
            location - string
            loc_type - string

    Outputs:
            City - string
            Code - string
            StateAbbreviation - string
            StateCode - string
    '''

    url1 = url_1(location, loc_type)
    loc_details = url_to_dict(url1)
    City = 'None'
    Code = 'None'
    StateAbbreviation = 'None' 
    StateCode = 'None'

    for loc in loc_details['Data']:
        if loc['Name'] == location and loc['StateAbbreviation'] == city_state[location]:
            City = loc['City']
            Code = loc['LocationCode']
            StateAbbreviation = loc['StateAbbreviation']
            StateCode = loc['StateCode']
    return  City, Code, StateAbbreviation, StateCode


def url_2(no_passenger, departOn, returnOn, originCity, originCode, originStateAbbreviation, originStateCode, destinationCity, destinationCode, destinationStateAbbreviation, destinationStateCode):
    '''
    Returns completed URL
    '''
    multi_word_origin = originCity.split()
    multi_word_destination = destinationCity.split()

    if len(multi_word_origin) == 2:
        originCity = multi_word_origin[0]+"+"+multi_word_origin[1]
    if len(multi_word_destination) == 2:
        destinationCity = multi_word_destination[0]+"+"+multi_word_destination[1]
    return "https://pegasus.greyhound.com/GhWebsite/schedules?originCity=%(originCity)s&originCode=%(originCode)s&destinationCity=%(d_city)s&destinationCode=%(d_code)s&departOn=%(departOn)s&returnOn=%(returnOn)s&totalPassengers=%(no_passenger)s+Passengers&adults=%(no_passenger)s&adultWheelchairs=0&children=0&childWheelchairs=0&seniors=0&seniorWheelchairs=0&discountCode=&GetTotalPassengers=%(no_passenger)s&HasWheelchairTraveler=false&HasReturnFare=true&webOnly=true&originStateAbbreviation=%(o_state)s&originStateCode=%(o_state_code)s&destinationStateAbbreviation=%(d_state)s&destinationStateCode=%(d_state_code)s"%{'originCity': originCity, 'originCode': originCode, 'o_state': originStateAbbreviation, 'o_state_code': originStateCode, 'no_passenger': no_passenger, 'departOn': departOn, 'returnOn': returnOn, 'd_city': destinationCity, 'd_code': destinationCode, 'd_state': destinationStateAbbreviation, 'd_state_code': destinationStateCode}


def grey_url(origin, destination, no_passenger, departOn, returnOn):
    '''
    This function returns the schedule of greyhound buses given the origin, the destination,
    the number of passengers, the departure date, and the return date.

    Input:
        all strings

    Output:
        tuple - containing all the details
    '''
    originCity, originCode, originStateAbbreviation, originStateCode = extract_from_url1(origin, "Origin")
    destinationCity, destinationCode, destinationStateAbbreviation, destinationStateCode = extract_from_url1(destination, "Destination")
    if destinationCity != 'None':
        url2 = url_2(no_passenger, departOn, returnOn, originCity, originCode, originStateAbbreviation, originStateCode, destinationCity, destinationCode, destinationStateAbbreviation, destinationStateCode)
        all_details = url_to_dict(url2)
        return all_details['Data']['Schedules'][0]["OnlineFares"]["Economy"]["FareTotal"]
    else:
        return 'None'


def find_greyhound_station(city):
    '''
    Returns latitude and longitude of greyhound station.

    Input:
        city - string

    Output:
        bus_st_geo - tuple
    '''
    url1 = url_1(city, "Destination")
    loc_details = url_to_dict(url1)
    for loc in loc_details['Data']:
        if loc['Name'] == city and loc['StateAbbreviation'] == city_state[city]:
            bus_st_zip = loc['ZipCode']
    bus_st_geo = get_lat_lng(bus_st_zip)
    return bus_st_geo


############################# YELP - HOTELS ################################
def hotel_search(lat, lon, price):
    '''
    This function will take a lat/lon (of a school)
    and price ('1' ($), '2'($$), '3'($$$)).
    
    Returns:
        Top 5 hotels that are closest to the university
        Top 5 rated hotels that are closest to the university (sort on rating, then on distance)
    
    '''
    database = pd.read_csv("CPS_Final_Data_Pandas.csv")
    hotels_dict = search(BEARER_TOKEN, 'Hotel', lat, lon, price)
    
    hotel_info_list = []

    for i in range(len(hotels_dict['businesses'])):
        if hotels_dict['businesses'][i]['categories'][0]['alias'] == 'hotels' \
        and hotels_dict['businesses'][i]['is_closed'] == False:
            name = hotels_dict['businesses'][i]['id']
            distance = hotels_dict['businesses'][i]['distance']
            rating = hotels_dict['businesses'][i]['rating']
            hotel_info_list.append((name,distance,rating))
    
    rating_list = sorted(hotel_info_list, key=itemgetter(2), reverse=True)[:5] #sorts by highest rating
    final_rating_list = sorted(rating_list, key=itemgetter(1)) #sorts highest rating with shortest distance

    if price == '1':
        price = "$"
    
    if price == '2':
        price = "$$"
    
    if price == '3':
        price = "$$$"

    city = list(database[database["Latitude"] == lat]['City'])[0]

    cost_of_hotel = hotel_prices_dict[city][price]

    hotel_list = []

    for hotel_name, distance, rating in final_rating_list:

        output_dict = get_business(BEARER_TOKEN, hotel_name)

        lat = output_dict['coordinates']['latitude'] #need for uber
        lon = output_dict['coordinates']['longitude'] #need for uber
        hotel_name = output_dict['name']
        proximity = distance*0.000621371 #converting to miles
        address = output_dict['location']['display_address'][0] + " " + output_dict['location']['display_address'][1]
        phone = output_dict['phone']
        price = cost_of_hotel
        rating = output_dict['rating']

        if len(phone) == 0:
            phone = "N/A"

        sub_list = [hotel_name, address, phone, price, rating, round(proximity,2)]
        hotel_list.append(sub_list)
    return hotel_list


################GREYHOUND CITY_STATE DICT##############
city_state = {'Allendale': 'MI',
 'Ames': 'IA',
 'Ann Arbor': 'MI',
 'Atlanta': 'GA',
 'Aurora': 'IL',
 'Beloit': 'WI',
 'Bloomington': 'IN',
 'Cambridge': 'MA',
 'Carbondale': 'IL',
 'Carlinville': 'IL',
 'Cedar Rapids': 'IA',
 'Champaign': 'IL',
 'Charleston': 'IL',
 'Chicago': 'IL',
 'Cicero': 'IL',
 'Columbia': 'MO',
 'Coraopolis': 'PA',
 'DeKalb': 'IL',
 'Decatur': 'IL',
 'Des Plaines': 'IL',
 'Downers Grove': 'IL',
 'Dubuque': 'IA',
 'East Lansing': 'MI',
 'Edwardsville': 'IL',
 'Elmhurst': 'IL',
 'Evanston': 'IL',
 'Fairfield': 'AL',
 'Fayette': 'IA',
 'Galesburg': 'IL',
 'Glen Ellyn': 'IL',
 'Graham': 'IL',
 'Granville': 'OH',
 'Greencastle': 'IN',
 'Holland': 'MI',
 'Huntsville': 'AL',
 'Iowa City': 'IA',
 'Ithaca': 'NY',
 'Jackson': 'MS',
 'Jacksonville': 'IL',
 'Joliet': 'IL',
 'Kenosha': 'WI',
 'Lake Forest': 'IL',
 'Lexington': 'KY',
 'Lincoln': 'IL',
 'Lincoln University': 'PA',
 'Little Rock': 'AR',
 'Los Angeles': 'CA',
 'Macomb': 'IL',
 'Madison': 'WI',
 'Malta': 'IL',
 'Milwaukee': 'WI',
 'Monmouth': 'IL',
 'Montgomery': 'AL',
 'Mount Pleasant': 'MI',
 'Muncie': 'IN',
 'Nashville': 'TN',
 'New York': 'NY',
 'Normal': 'IL',
 'Northfield': 'MN',
 'Oberlin': 'OH',
 'Palatine': 'IL',
 'Palos Hills': 'IL',
 'Peoria': 'IL',
 'Pine Bluff': 'AR',
 'Portland': 'OR',
 'Quincy': 'IL',
 'River Forest': 'IL',
 'Romeoville': 'IL',
 'South Holland': 'IL',
 'Springfield': 'IL',
 'St. Louis': 'MO',
 'Terre Haute': 'IN',
 'Tougaloo': 'MS',
 'Tuskegee': 'AL',
 'University Park': 'IL',
 'Urbana': 'IL',
 'Valparaiso': 'IN',
 'Vincennes': 'IN',
 'Wilberforce': 'OH'}


##########THIS IS THE AIRDICT REQUIRED FOR THE PRICING ALOGRITHM#############
air_dict = {"JP": "Adria Airways",
"NK": "Spirit Airlines",
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
"F9": "Frontier Airlines",
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
"VG": "VLM Airlines (Cityjet)",
"VX": "Virgin America"}