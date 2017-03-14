from All_Helper import *
from datetime import *
import pandas as pd


def get_itinerary(itin_input):
    '''
    Receives input dictionary from Django and returns a tuple of dictionaries. The first will be the 
    return dictionary, with new information to send to Django, and the second is the input 
    dictionary 

    itin_input example = 
    {'home_addr': '945 E 52nd St Chicago',
    'school1': 'CITY OF CHICAGO - HAROLD WASHINGTON COLL',
    'depart_home': datetime.date(2017, 4, 12), 
    'depart_school1': datetime.date(2017, 4, 16), 
    'hotel_pref': '$$$', 
    'num_travelling': 3,
    'school2': 'Name of College',    
    'depart_school2': None} 

    $12 per person per day per meal for meals ($36 total)

    Input:
        itin_input - dictionary

    Return: 
        return_dict - dictionary 
        itin_input
    '''
    #Home location
    home_lat, home_lng = get_lat_lng(itin_input['home_addr'])

    #Calculate number of days
    num_days = (itin_input['depart_school1'] - itin_input['depart_home']).days

    #Get values
    num_people = itin_input['num_travelling']
    price = itin_input['hotel_pref']

    #Calculate meal cost
    cost_meal = 36 * num_people * num_days

    #Dictionary to return
    return_dict = {'food':0, 'uber':0, 'bus':0, 'hotels':[], 'flights':[]}

    if itin_input['school2'] == 'Name of College':  #Only one school selected
        school = itin_input['school1']

        # School State
        cps_schools = pd.read_csv('CPS_Final_Data_Pandas.csv')
        sch_row = cps_schools['Name of College'] ==  school
        school_state = list(cps_schools[sch_row]['State'])[0]

        
        date1 = str(itin_input['depart_home']).split()[0]
        date2 = str(itin_input['depart_school1']).split()[0]
        
        #Calculate distance to school through latitude and longitude
        school_lat, school_lng = get_lat_lng_file(school)
        distance_str = get_distance(home_lat, home_lng, school_lat, school_lng)
        distance = float(distance_str[:-3])

        #Calculate costs depending on distance
        if distance <= 50: #Uber to school
            cost_uber = uber_ride(home_lat, home_lng,school_lat, school_lng)
            cost_uber = cost_uber * 2  #roundtrip
            cost_uber = cost_uber * num_days
            return_dict['uber'] = cost_uber
            return_dict['food'] = cost_meal
            
            return (return_dict, None)
            
        elif distance > 50 and distance <= 100: #Bus to school         
            bus_st_lat, bus_st_lng = find_greyhound_station('Chicago')
            cost_uber1 = uber_ride(home_lat, home_lng, bus_st_lat, bus_st_lng) #Uber home to bus station

            school_city = get_city(school)
            greyhound_cost = grey_url('Chicago', school_city, num_people, date1, date1) #Greyhound to school city
            
            if greyhound_cost == 'None':  #If no greyhound bus in city, use an estimate
                greyhound_cost = int((9 + (0.08 * distance)) * num_people)
                cost_uber2 = 7

            else: 
                sch_bus_lat, sch_bus_lng = find_greyhound_station(school_city)
                cost_uber2 = uber_ride(sch_bus_lat,sch_bus_lng,school_lat,school_lng) #Uber bus station to school        
            
            total_uber_cost = (cost_uber1 * 2) + (cost_uber2 * 2) * num_days 
            total_greyhound_cost = greyhound_cost * 2 * num_days  #Roundtrip on num_days

            return_dict['uber'] = total_uber_cost
            return_dict['bus'] = total_greyhound_cost
            return_dict['food'] = cost_meal

            return (return_dict, None)

        elif distance > 100 and distance <= 150:  #Bus, hotel

            hotel_list = hotel_search(school_lat, school_lng, price)
            return_dict['hotels'] = hotel_list

            return return_dict, itin_input

        elif distance > 150:  #Flight, hotel

            if school_state == 'IL':
                hotel_list = hotel_search(school_lat, school_lng, price)
                return_dict['hotels'] = hotel_list

                return return_dict, itin_input

            else:
                depart_date = date1
                return_date = date2
                destination = get_airport(school)
                flight_list = find_flights('CHI', destination, depart_date, return_date, num_people)
                hotel_list = hotel_search(school_lat, school_lng, price)

                return_dict['hotels'] = hotel_list
                return_dict['flights'] = flight_list

                return return_dict, itin_input

    #else:  #If two schools
    #    return get_itin_two_schools(itin_input)


def get_rest_itin(itin_input_original, itin_input_choice):
    '''
    Given the original dictionary, and the second dictionary created by Django containing
    additional choice, this function returns the full cost dictionary, to create the treemap

    Inputs:
        itin_input_original - dictionary
        itin_input_choice - dictionary 

    Output:
        final_cost_dict - dictionary

    '''
    #Home location
    home_lat, home_lng = get_lat_lng(itin_input_original['home_addr'])

    #Calculate number of days
    num_days = (itin_input_original['depart_school1'] - itin_input_original['depart_home']).days

    #Get values
    num_people = itin_input_original['num_travelling']
    price = itin_input_original['hotel_pref']
    hotel_choice = ast.literal_eval(itin_input_choice['hotel'])
    hotel_cost = (hotel_choice[3]) * num_days
    hotel_lat, hotel_lng = get_lat_lng(hotel_choice[1])
    school = itin_input_original['school1']
    school_lat, school_lng = get_lat_lng_file(school)

    #Calculate meal cost
    cost_meal = 36 * num_people * num_days

    #Final return dictionary
    final_cost_dict = {'food':0, 'uber':0, 'bus':0, 'hotels':0, 'flights':0}

    if itin_input_original['school2'] == 'Name of College':  #Only one school selected
        #School
        school = itin_input_original['school1']
                
        if 'flight' not in itin_input_choice: #Bus and hotel             
            date1 = str(itin_input_original['depart_home']).split()[0]
            bus_st_lat, bus_st_lng = find_greyhound_station('Chicago')
            cost_uber1 = uber_ride(home_lat, home_lng, bus_st_lat, bus_st_lng) #Uber home to bus station

            school_city = get_city(school)
            greyhound_cost = grey_url('Chicago', school_city, num_people, date1, date1) #Greyhound to school city
            if greyhound_cost == 'None':  #If no greyhound bus in city, use an estimate
                school_lat, school_lng = get_lat_lng_file(school)
                distance_str = get_distance(home_lat, home_lng, school_lat, school_lng)
                distance = float(distance_str[:-3])
                greyhound_cost = int((9 + (0.08 * distance)) * num_people)
                cost_uber2 = 7
            
            else:  #If greyhound available
                sch_bus_lat, sch_bus_lng = find_greyhound_station(school_city)
                cost_uber2 = uber_ride(sch_bus_lat,sch_bus_lng,hotel_lat,hotel_lng) #Uber bus station to hotel             
            
            cost_uber3 = uber_ride(hotel_lat,hotel_lng,school_lat,school_lng) #Uber hotel to school

            total_uber_cost = (cost_uber1 * 2) + (cost_uber2 * 2) + (cost_uber3 * 2 * num_days)
           
            total_greyhound_cost = greyhound_cost * 2

            final_cost_dict['food'] = cost_meal
            final_cost_dict['uber'] = total_uber_cost
            final_cost_dict['bus'] = total_greyhound_cost
            final_cost_dict['hotels'] = hotel_cost
            
            return final_cost_dict

        else:  #Flight and hotel
            airports_database = pd.read_csv('airport_data_final_pandas_database.csv')
            flight_choice = ast.literal_eval(itin_input_choice['flight'])
            airport_code = flight_choice[0][1]
            
            home_air_lat = float(airports_database[airports_database['FAA'] == airport_code]['Latitude'])
            home_air_lng = float(airports_database[airports_database['FAA'] == airport_code]['Longitude'])

            cost_uber1 = uber_ride(home_lat, home_lng, home_air_lat, home_air_lng) #Uber home to airport

            school_city = get_city(school)
            school_lat, school_lng = get_lat_lng_file(school)

            flight_cost = int(flight_choice[0][0])

            school_air_code = flight_choice[0][3]
            school_air_lat = float(airports_database[airports_database['FAA'] == school_air_code]['Latitude'])
            school_air_lng = float(airports_database[airports_database['FAA'] == school_air_code]['Longitude'])

            air_to_school_dist_str = get_distance(school_air_lat, school_air_lng, school_lat, school_lng)
            air_to_school_dist = float(air_to_school_dist_str[:-3])

            if air_to_school_dist <= 50:  #Take Uber
                #print("school_air_lat,school_air_lng,hotel_lat,hotel_lng", school_air_lat,school_air_lng,hotel_lat,hotel_lng)
                cost_uber2 = uber_ride(school_air_lat,school_air_lng,hotel_lat,hotel_lng) #Uber airport to hotel             
                #print("hotel_lat,hotel_lng,school_lat,school_lng", hotel_lat,hotel_lng,school_lat,school_lng)
                cost_uber3 = uber_ride(hotel_lat,hotel_lng,school_lat,school_lng) #Uber hotel to school
                
            else: #Take bus
                greyhound_cost = int((9 + (0.08 * air_to_school_dist)) * num_people)
                cost_uber2 = 7
                cost_uber3 = 7
                final_cost_dict['bus'] = greyhound_cost

            total_uber_cost = (cost_uber1 * 2) + (cost_uber2 * 2) + (cost_uber3 * 2 * num_days)

            final_cost_dict['food'] = cost_meal
            final_cost_dict['uber'] = total_uber_cost
            final_cost_dict['flights'] = flight_cost
            final_cost_dict['hotels'] = hotel_cost

    return final_cost_dict


'''
def get_itin_two_schools(itin_input):
    elif itin_input['num_schools'] == 2:
        school_a_lat, school_a_lng = get_lat_lng_file(itin_input['name_school'][0])
        school_b_lat, school_b_lng = get_lat_lng_file(itin_input['name_school'][1])

        distance_h2a_str = get_distance(home_lat, home_lng, school_a_lat, school_a_lng)
        distance_h2a = float(distance_h2a_str[:-3])

        distance_h2b_str = get_distance(home_lat, home_lng, school_b_lat, school_b_lng)
        distance_h2b = float(distance_h2b_str[:-3])

        distance_a2b_str = get_distance(school_a_lat, school_a_lng, school_b_lat, school_b_lng)
        distance_a2b = float(distance_a2b_str[:-3])
  
        if distance_h2a <= 100 and distance_h2b <= 100: #Only day trips
            if distance_h2a <= 50: #Uber h2a

                if distance_h2b <= 50: #Uber h2b
                    #add Uber h2a + Uber h2b

                elif distance_h2b > 50 and distance_h2b <= 100: #Bus h2b
                    #add Uber h2a + Bus h2b

        else: #At least one >100
            if distance_h2a <= 50: #Uber h2a (no hotel @a)

                if distance_h2b > 100 and distance_h2b <= 150: #Bus h2b, hotel
                    #add Uber h2a + Bus h2b + Hotel @b

                if distance_h2b > 150: #Bus/flight h2b, Hotel @b
                    #add Uber h2a + Bus/flight h2b_rt + Hotel Hotel @b

            elif distance_h2a > 50 and distance_h2a <= 100: #Bus h2a (no hotel @a)

                if distance_h2b > 100 and distance_h2b <= 150: #Bus h2b, Hotel @b
                    #add Bus h2a + Bus h2b + Hotel @b

                if distance_h2b > 150:  #Bus/flight h2b, Hotel @b
                    #add Bus h2a + Bus/flight h2b_rt + Hotel @b

            elif distance_h2a > 100 and distance_h2a <= 150:  #Bus h2a, Hotel 

                if distance_a2b <= 30: #Same hotel
                    #add Bus h2a, Hotel a+b

                elif distance_a2b > 30 and distance_a2b <= 50: #Different hotel
                    #add Bus h2a + Hotel @a + Uber + Hotel @b

                elif distance_a2b > 50 and distance_a2b <= 150: #Bus a2b, Hotel @a
                    #add Bus h2a + Hotel @a + Bus a2b + Hotel @b

                elif distance_a2b > 150: #Bus/Flight, Hotel @b
                    #add Bus h2a + Hotel @a + Bus/Flight a2b_b2h + Hotel @b

            elif distance_h2a > 150: #Bus/flight h2a, Hotel

                if distance_a2b <= 30: #Same hotel
                    #add Bus/Flight h2a_rt, Hotel a+b

                elif distance_a2b > 30 and distance_a2b <= 50: #Different hotel
                    #add Bus/Flight h2a_rt + Hotel @a + Uber + Hotel @b

                elif distance_a2b > 50 and distance_a2b <= 150: #Bus a2b, Hotel @b
                    #add Bus/flight h2a_rt + Hotel @a + Bus a2b + Hotel @b

                elif distance_a2b > 150:  #Bus/Flight a2b, Hotel @b
                    #add Bus/flight h2a_a2b_b2h + Hotel @a + Hotel @b
'''





