import streamlit
import pandas
import requests
import snowflake.connector
#from streamli.error import URLerror


streamlit.title('Healthy Dinner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 and blueberry Oatmeal')
streamlit.text('🥗 Smoothie')
streamlit.text('Juice')
streamlit.text('🥑🍞Avacado toast')
streamlit.text('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
streamlit.title('New Healthy Dinner')



#my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
## Display the table on the page.
#streamlit.dataframe(my_fruit_list)
#
#
#my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
##create index on fruits
#my_fruit_list = my_fruit_list.set_index('Fruit')
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
## Display the table on the page.
#streamlit.dataframe(my_fruit_list)
#
#
#my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
##create index on fruits
#my_fruit_list = my_fruit_list.set_index('Fruit')
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
## Display the table on the page.
#streamlit.dataframe(my_fruit_list)


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#create index on fruits
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruityvice_response.json())

## write your own comment -what does the next line do? 
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
## write your own comment - what does this do?
#streamlit.dataframe(fruityvice_normalized)


fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.header("The fruit_load_list contains: ")
#streamlit.text("The fruit_load_list contains: ")
#streamlit.text(my_data_row)
streamlit.dataframe(my_data_row)



my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit_load_list contains: ")
#streamlit.text("The fruit_load_list contains: ")
streamlit.dataframe(my_data_rows)
fruit_choice = streamlit.text_input('What fruit would you like to add?')
streamlit.write('Thanks for adding ', fruit_choice)

my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")



streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
  else:
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      streamlit.dataframe(fruityvice_normalized)
except URLError as e:
    streamlit.error()                      

    
  
#Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx_cursor() as my_cur:
         my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values (new_fruit)")
         return "Thanks for adding " + new_fruit


streamlit.header("View our Fruit list - Add your favorits")
if streamlit.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)
  
