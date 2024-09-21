# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Custamize Your Smoothie :balloon:")
st.write(
   """choose the fruit that you want in custom smoothie!"""
)

name_on_order = st.text_input('Name on Smoothie:')

st.write('The name on your Smoothie will be:', name_on_order)
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect( 'Choose up to 5 ingredients:' ,my_dataframe)
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string =''
    for fruit_chosen in ingredients_list: 
        ingredients_string += fruit_chosen + ' '
    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order) 
                    values ('""" +ingredients_string+ """','""" +name_on_order+ """')"""

    #st.write(my_insert_stmt)
    st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
# Show a message if more than 5 ingredients are selected
if len(ingredients_list) > 5:
    st.warning("You can only select up to 5 options. Remove an option first.")

