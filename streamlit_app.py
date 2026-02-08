# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customise Your Smoothie")
st.write(
  """Choose the fruit you want in your smoothie.
  """
)

order_name = st.text_input("Your Name")
st.write("The name on your smoothie will be:", order_name)

# Import data
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

# Multiselect
ingredients = st.multiselect(
    "Choose your ingredients.",
    my_dataframe,
    max_selections= 6
    #default=["Apples", "Figs"],
)

if ingredients:

    ingredients_string = ''

    for fruit_chosen in ingredients:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into SMOOTHIES.PUBLIC.ORDERS(ingredients, order_name)
                values ('""" + ingredients_string + """', '"""+order_name+ """')"""
    
    #st.write(my_insert_stmt)
    #st.stop()

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered {order_name}.", icon="✅")

  
