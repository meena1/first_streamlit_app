
import streamlit
import pandas 
import snowflake.connector
import requests
from urllib.error import URLError

streamlit.title("My parents new healthy dinner")
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

def func_fruit(x):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+x)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")

try : 
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("please enter fruit name to get information")
  else:
    y = fun_fruit(fruit_choice)
    streamlit.dataframe(y)
    
except URLerror as e:
  streamlit.error()
  
streamlit.stop()
  
#streamlit.text(fruityvice_response.json())

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("use warehouse pc_rivery_wh")
my_cur.execute("SELECT * from fruit_load_list")
my_data = my_cur.fetchall()
streamlit.text("List:")
streamlit.dataframe(my_data)

fruit_choice_1 = streamlit.text_input('What fruit would you like to add- ?')

my_cur.execute("insert into fruit_load_list values("+fruit_choice_1+")")

streamlit.write('Thanks for adding ', fruit_choice_1)
