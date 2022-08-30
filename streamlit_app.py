import streamlit as sl
import pandas as pd

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
fruits_selected = sl.multiselect("Pick some fruits:", list(my_fruit_list.index),['Apple','Banana'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
# calling dataframe
sl.dataframe(fruits_to_show)
