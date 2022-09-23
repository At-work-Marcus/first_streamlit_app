import streamlit as sl
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

# create title
sl.title('My Parents Healthy Diner')
# create header and sub text
sl.header('🥚 Breakfast favorites ☕')
sl.text('🥛 smoothie')
sl.text('🥙 pancakes')
sl.text('🍞 hard boiled egg')

# new header
sl.header('🍌 Build your own smoothie  🍓')

# reading in csv
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
# list of pre-selected fruits
pre_selected = ['Apple','Banana','Avocado']
fruits_selected = sl.multiselect("Pick some fruits:", list(my_fruit_list.index),pre_selected)
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
# calling dataframe
sl.dataframe(fruits_to_show)

# lesson 9 Snowflake DABW
# creating fxn to call data from FDC
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized


# creating variable for user input
sl.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = sl.text_input('What fruit would you like information about?')
  # sl.write('The user entered ', fruit_choice) # old line before try except
  # using that input to call the data for that fruit 
  if not fruit_choice:
    sl.error('Please select a piece of fruit to get info about.')
  else:
    back_from_fxn = get_fruityvice_data(fruit_choice)
    # sl.text(fruityvice_response.json()) # << just writes the data to the screen in json format
    # normalizing requested json data w/ pandas
    # fruityvice_normalized = pd.json_normalize(fruityvice_response.json()) # moved this to the get_fruityvice_data fxn
    # puts data in a better view in the app
    sl.dataframe(back_from_fxn)
except URLError as e:
  sl.error()
  

# stopping while troubleshooting 9/22/2022
#sl.stop()

# lesson 12 DABW reading data from Snowflake into streamlit app
# fxn to call data from fruit_load_list
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

if sl.button('Get fruit load list'):
  my_cnx = snowflake.connector.connect(**sl.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  sl.dataframe(my_data_rows)


sl.write('Thanks for adding ', add_my_fruit)

# adding fxn to add fruit to snowflake fruit_load_list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('" + new_fruit + "')")
    return "Thanks for adding " + new_fruit

# add second text entry box
add_my_fruit = sl.text_input('What fruit would you like to add')
if sl.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**sl.secrets["snowflake"])
  back_from_fxn = insert_row_snowflake(add_my_fruit)
