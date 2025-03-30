##🥋Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
#🥋 Let's Call the SmoothieFroot API from Our SniS App!
import requests


##2 🥋 Write directly to the app
st.title("Customize ur app Smoothies:cup_with_straw:")
st.write("Chose the fruits you xant in ur custom Smoothie:")

## 10 🥋 Add a Name Box for Smoothie Orders
## **https://docs.streamlit.io/develop/api-reference/widgets/st.text_input**

title = st.text_input("Name of the smoothie : ")
st.write("The of your Name of the smoothie is", title)

##3🥋 Activate a table & select column
cnx= st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)


##4🥋 Add a Multiselect
ingredients_list = st.multiselect(
        "Chose up until 5 ingredients"
        ,my_dataframe    #<-format_func
        ,max_selections =5 
    )

#We are placing the multiselect entries into a variable called "ingredients." We can then write "ingredients" back out to the screen.
#Our ingredients variable is an object or data type called a LIST. So it's a list in the traditional sense of the word, but it is also a datatype or object called a LIST. A LIST is different than a DATAFRAME which is also different from a STRING!
#We can use the st.write() and st.text() methods to take a closer look at what is contained in our ingredients LIST. "

if ingredients_list:
    ingredients_string = ''
    name_on_order = title
##🥋5 Create a Place to Store Order Data (see DABW WokrSheet)

##🥋6 Create the INGREDIENTS_STRING Variable 
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        #🥋10.3 Use Our fruit_chosen Variable in the API Call
        st.subheader(fruit_chosen + 'Nutrition Information')
        
        #10.2🥋 Let's Get the SmoothieFroot Data to Show Nutrition Data for the Fruits Chosen
        #smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/orange")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    #st.text(ingredients_string)

##7 🥋 Build a SQL Insert Statement & Test It
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
    #st.write(my_insert_stmt)

##🥋8 Insert the Order into Snowflake
    #if ingredients_string:
        #session.sql(my_insert_stmt).collect()
        #st.success('Your Smoothie is ordered!', icon="✅")

## 🥋 Truncate the Orders Table (see DABW WokrSheet : TRUNCATE table smoothies.public.orders;)

## 9 🥋 Add a Submit Button
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}', icon="✅")

## 11.🥋 Use the ALTER Command to Add a New Column to Your Orders Table ((see DABW WokrSheet))
## ALTER TABLE smoothies.public.orders add column Name varchar(100);

## 🥋 add new section to show smoothie fruit nutrition information
#smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/orange")
#st.text(smoothiefroot_response)

## 🥋 Expose the JSON Data Inside the Response Object
#st.text(smoothiefroot_response.json())

## 🥋 Let's Put the JSON into a Dataframe
#sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
