import pickle
import datetime
import pandas as pd
import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import (LoginError)

st.title("Home Sale Price Prediction Tool")
st.subheader("For predicting sale prices of homes in Fairfax County, Virginia.")
st.write("Application written for the fictitious Conner Investment Group, LLC. For academic use only.")

with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

with open('home_sales_lr_model.pkl', 'rb') as file:
    price_prediction_model = pickle.load(file)

median_price_by_zip = pd.read_csv('./data/median_price_by_zip.csv')
input_data = [0, 0, 0, 0, '', 0, 0]


def prepare_user_input(user_input):
    user_input[4] = pd.to_datetime(user_input[4]).toordinal()
    user_input[6] = median_price_by_zip.loc[median_price_by_zip["zip_code"] == user_input[6]]['median_price'].values[0]
    return user_input

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

try:
    authenticator.login()
except LoginError as e:
    st.error(e)

if st.session_state["authentication_status"]:
    st.write('___')
    with st.form('real_estate_data', clear_on_submit=False, enter_to_submit=False):
        input_data[0] = st.number_input("Year built:", value=int(0), key="year_built")
        input_data[1] = st.number_input("Interior area (sqft):", value=int(0), key="interior_area")
        input_data[2] = st.selectbox("Bedrooms:", (1,2,3,4,5,6,7,8,9), index=None, key="bedrooms")
        input_data[3] = st.selectbox("Full baths:", (1,2,3,4,5,6,7,8,9), index=None, key="baths")
        input_data[4] = st.date_input("Sale date:", datetime.date.today(), key="sale_date")
        input_data[5] = st.number_input("Lot size (acres):", value=float(0.0), key="lot_size")
        input_data[6] = st.selectbox("Zip code:", options=median_price_by_zip['zip_code'], key="zip_code")

        if 'button_clicked' not in st.session_state:
            st.session_state.button_clicked = False

        def handle_click():
            st.session_state.button_clicked = True

        submitted = st.form_submit_button(on_click=handle_click)


        if submitted:
            formatted_input = prepare_user_input(input_data)
            predicted_price = price_prediction_model.predict([formatted_input])
            formatted_price = predicted_price.astype(float)[0][0]
            currency_string = f"${formatted_price:,.2f}"
            st.write(currency_string)


    st.write('___')
    authenticator.logout()

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

with open('config.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(config, file, default_flow_style=False)

