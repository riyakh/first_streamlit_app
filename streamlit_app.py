import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents new healthy Diner')
streamlit.header('Breakfast Favourites')
streamlit.text(' 🥣 Omega 3 & blueberry oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smothie')
streamlit.text(' 🐔 Hard-Boiled Free-range egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header('Fruityvice Fruit Advice')
def get_fruityvice_data(this_fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    #streamlit.text(fruityvice_response.json())
   fruitvice_normalised = pandas.json_normalize(fruityvice_response.json())
   return fruitvice_normalised
   
try:
  fruit_choice = streamlit.text_input("What fruit would you like to tte information about")
  if not fruit_choice:
    streamlit.error('please select fruit to get the information')
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    #streamlit.write('The user entered',fruit_choice)
    streamlit.dataframe(back_from_function)
   
except URLError as e:
  streamlit.error()
    


streamlit.header('The fruit load list contains')

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()
  
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)
#streamlit.stop()

#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT * from fruit_load_list")
#my_data_row = my_cur.fetchall()
#streamlit.header("The fruit load list contains:")

#streamlit.dataframe(my_data_row)

def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
      my_cur.execute('Insert into fruit_load_list values ("' + new_fruit +"')')
      return ('thanks for adding ' + new_fruit)

add_my_fruit=streamlit.text_input("what fruit would you like to add?")
if streamlit.button('Add a fruit'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_func = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_func)

#my_cur.execute("insert into fruit_load_list values ('from streamlit')")

