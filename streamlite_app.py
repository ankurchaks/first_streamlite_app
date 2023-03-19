import streamlit
import pandas
import requests
import snowflake.connector
#from urllib.error import URLError
from urllib.error import URLError

streamlit.title("My Mom's New Healthy Diner")

streamlit.header("🍔 Breakfast Menu")

streamlit.text("🧆 Omega 3 & Blueberry oatmeal")

streamlit.text("🥗 Kale, Spinach & Roket Smoothie")

streamlit.text("🥪 Hard-Boiled Free-Range egg")

streamlit.text("🥑 🍞 Avacado toast")

streamlit.header("🍌🥭 Make Your Own Smoothie 🥝🍇")

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.dataframe(my_fruit_list)

# Let's put a pick list here so they can pick the fruit they want to include
streamlit.title("Build Your Own Fruit Smoothie")
# streamlit.multiselect("Pick Some Fruits:", list(my_fruit_list.index))
# streamlit.multiselect("Pick Some Fruits:", list(my_fruit_list.index),["Avocado","Strawberries"])
fruits_selected=streamlit.multiselect("Pick Some Fruits:", list(my_fruit_list.index),["Avocado","Strawberries"])
fruits_to_show=my_fruit_list.loc[fruits_selected]

# Display the table on page
# streamlit.dataframe(my_fruit_list)

streamlit.dataframe(fruits_to_show)




def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

# New section to display Fruityvice API response
streamlit.header("Fruityvice Fruit Advice!")

try:
  fruit_choice=streamlit.text_input('What fruit would you like to have information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    back_from_function=get_fruityvice_data (fruit_choice)
    streamlit.dataframe(back_from_function)
 
except URLError as e:
  streamlit.error()
    
    
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# streamlit.text(fruityvice_response.json()) # Just write the data on the screen

#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
#fruit_choice=streamlit.text_input('What fruit would you like to have information about?', 'Kiwi')
#streamlit.write('The user entered', fruit_choice)

#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# take the json version of the response and normalize it
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

# Display the result on the screen as a table
# streamlit.dataframe(fruityvice_normalized)

streamlit.text("Data from snowSQL starts after this point")

streamlit.header("The fruit load list contains:")
# Snowflake-related functions

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("Select * FROM FRUIT_LOAD_LIST")
        return my_cur.fetchall()
    
# Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows=get_fruit_load_list()
    streamlit.dataframe(my_data_rows)
    
# Allow the user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list Values ('from steamlit')")
        return "Thanks for adding " + new_fruit

add_my_fruit=streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function=insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)

streamlit.stop()
streamlit.text("Data from snowSQL starts")


# Query Our Trial Account Metadata 
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("Select * FROM FRUIT_LOAD_LIST")
my_data_row = my_cur.fetchone()
streamlit.text("The fruit load list contains:")
streamlit.text(my_data_row)

# Change the Streamlit Components to Make Things Look a Little Nicer
my_data_row = my_cur.fetchone()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)

# Oops! Let's Get All the Rows, Not Just One
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains")
streamlit.dataframe(my_data_row)

# Add Text Entry Box
add_my_fruit=streamlit.text_input('What fruit would you like information about?')
streamlit.write('Thanks for adding', add_my_fruit)

# Add data to snowSQL Table 
my_cur.execute("insert into fruit_load_list Values ('from steamlit')")
