import streamlit
import pandas
import requests

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

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_response.json()) # Just write the data on the screen

# take the json version of the response and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

# Display the result on the screen as a table
streamlit.dataframe(fruityvice_normalized)
