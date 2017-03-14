
# coding: utf-8

# The code below was used to construct the database which matched the closest airport to each school. This was essential for our airlines algorithm in order to find the flights that students would take to a particular university.

# In[166]:

# import googlemaps
# gmaps = googlemaps.Client(key="AIzaSyA7CqI3UK8sWAmiApH9shd2M7Rl7acOBzo", timeout=None)
# import pandas as pd


# In[167]:

# college_database = pd.read_csv("college_distance.csv")


# In[168]:

# airport_database = pd.read_excel('Airport_Data.xlsx', encoding = 'latin-1')


# In[169]:

# airport_unclean_list = []
# for i in airport_database['Airport']:
#     airport_unclean_list.append(i)

# airport_clean_list = []
# for i in airport_unclean_list:
#     if u'\xa0' in i:
#         clean_it = i.replace(u'\xa0', u' ')
#         airport_clean_list.append(clean_it)
#     else:
#         airport_clean_list.append(i)


# In[170]:

# airport_database['Airport'] = airport_clean_list


# In[171]:

# airport_database.to_csv("airport_data_final_pandas_database.csv", index=False)


# In[172]:

# airport_database = pd.read_csv("airport_data_final_pandas_database.csv")


# In[173]:

# college_database_final = college_database[college_database["State"] != "IL"]


# In[174]:

# college_lat = list(college_database_final["Latitude"])
# college_lon = list(college_database_final["Longitude"])
# college_name = list(college_database_final["Name of College"])

# airport_lat = list(airport_database["Latitude"])
# airport_lon = list(airport_database["Longitude"])
# airport_name = list(airport_database["Airport"])
# airport_code = list(airport_database["FAA"])

# college_tuples = list(zip(college_lat,college_lon, college_name))

# airport_tuples = list(zip(airport_lat, airport_lon, airport_name, airport_code))


# In[175]:

# distance_list = []
# final_airport_name = []
# final_airport_lat = []
# final_airport_lon = []
# final_airport_code = []
# for c_tuples in college_tuples:
#     c_lat, c_lon, c_name = c_tuples
#     distance_list = []
#     for a_tuples in airport_tuples:
#         a_lat,a_lon, a_name, a_code = a_tuples
#         matrix = gmaps.distance_matrix((c_lat, c_lon),(a_lat, a_lon),mode = "driving", units ="imperial")
#         distance = matrix["rows"][0]['elements'][0]['distance']['value']
#         distance_list.append((distance, a_name, str(a_lat), str(a_lon), a_code))
#     sort = sorted(distance_list, key=lambda x:x[0])
#     final_airport_name.append(sort[0][1])
#     final_airport_lat.append(sort[0][2])
#     final_airport_lon.append(sort[0][3])
#     final_airport_code.append(sort[0][4])


# In[176]:

# airport_latitude = [float(x) for x in final_airport_lat]
# airport_longitude = [float(x) for x in final_airport_lon]


# In[177]:

# final_data = {"College": list(college_database_final["Name of College"]),
#               'Airport_Name': final_airport_name,
#               "Airport_Code" : final_airport_code,
#               'Latitude': airport_latitude,
#               'Longitude': airport_longitude}

# airport_distance_final_pandas = pd.DataFrame(final_data)


# In[178]:

# airport_distance_final_pandas.to_csv("airport_distance_final_pandas_database.csv", index=False)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



