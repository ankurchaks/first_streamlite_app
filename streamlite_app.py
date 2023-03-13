import streamlit
import pandas
import requests
import snowflake.connector

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
# streamlit.multiselect("Pick Some Fruits:", list(my_fruit_list.index))
# streamlit.multiselect("Pick Some Fruits:", list(my_fruit_list.index),["Avocado","Strawberries"])
fruits_selected=streamlit.multiselect("Pick Some Fruits:", list(my_fruit_list.index),["Avocado","Strawberries"])
fruits_to_show=my_fruit_list.loc[fruits_selected]

# Display the table on page
# streamlit.dataframe(my_fruit_list)

streamlit.dataframe(fruits_to_show)


# New section to display Fruityvice API response
streamlit.header("Fruityvice Fruit Advice!")

#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# streamlit.text(fruityvice_response.json()) # Just write the data on the screen

#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
fruit_choice=streamlit.text_input('What fruit would you like to have information about?', 'Kiwi')
streamlit.write('The user entered', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# take the json version of the response and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

# Display the result on the screen as a table
streamlit.dataframe(fruityvice_normalized)

# Let's Query Our Trial Account Metadata 
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

# Let's Query Some Data, Instead
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.text("The fruit load list contains")
streamlit.text(my_data_row)

# Let's Change the Streamlit Components to Make Things Look a Little Nicer
my_data_row = my_cur.fetchone()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)

# Oops! Let's Get All the Rows, Not Just One
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.text("The fruit load list contains")
streamlit.text(my_data_row)
streamlit.dataframe(my_data_row)


streamlit.text_input("What fruit would you like to add?")

