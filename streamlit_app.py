import streamlit
#import pandas
#import requests
from urllib.error import URLError
streamlit.title('My parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & rocket smothie')
streamlit.text('🐔 Hard-boiled Free-Range egg')
streamlit.text('🥑🍞 Avocado toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv( "https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits: ", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_response.json())

fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
 
#Try catch exemption
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()

#streamlit.stop()

import snowflake.connector
#snowflake-realted functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("Select * from fruit_load_list")
        return my_cur.fetchall()
#allow the user to add a fruit to the list
def insert_rows_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruitLoad_list values('" + new_fruit + "')")
        return "Thanks for adding " + new_fruit
    
 add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)
    
    
# add button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)                      

    
streamlit.stop()
#my_cur = my_cnx.cursor()
##my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_cur.execute("select * from fruit_load_list")
#my_cur.execute("insert into fruit_load_list values ('centeloupe')")
#my_data_row = my_cur.fetchall()

#streamlit.text("The fruit load list: :")
#streamlit.text(my_data_row)
#streamlit.header ("The fruit load list contain")
#streamlit.dataframe(my_data_row)

#add_fruit = streamlit.text_input("What fruit would you like to add? ", 'Jackfruit')
#streamlit.text ('Thnak you for adding ' + add_fruit)
