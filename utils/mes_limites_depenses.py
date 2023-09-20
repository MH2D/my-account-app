import streamlit as st
import pandas as pd
from utils.my_variables import *

from utils.global_utils import *


def questionnaire_category(USERNAME):
    category_list = list(CATEGORIES['expenses'].keys())
    limits_df = read_csv_from_gcs(f'{USERNAME}_budget_limits.csv', bucket_name=BUCKET_NAME)
    limits_df['category'] = category_list
    
    limit_categories = {}
    for cat in category_list:
        limit_categories[cat] = st.number_input(cat, min_value=5)
        
    if st.button('Update your budget limits'):

        for cat, lim in limit_categories.items():
            limits_df.limit = limits_df.category.apply(lambda x: lim)

        write_csv_to_gcs(limits_df, f'{USERNAME}_budget_limits.csv', bucket_name=BUCKET_NAME)

    st.table(limits_df)