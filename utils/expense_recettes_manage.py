import streamlit as st
import pandas as pd
from utils.my_variables import *

from utils.global_utils import *



# Define a function to add new expenses
def add_expense():

    # st.header("Add New Expense")

    # Form inputs for adding a new expense
    spending_date = st.date_input("Date")
    description = st.text_input("Description")
    # Get the list of categories
    category_list = list(CATEGORIES['expenses'].keys())
    selected_catego = st.selectbox("Select Category", category_list)

    selected_subcategories = CATEGORIES['expenses'].get(selected_catego, [])
    sub_category = st.selectbox("Select Sub Category", selected_subcategories)
    amount = st.number_input("Amount", min_value=0.1)

    # Add the new expense to the database
    if st.button("Add Expense"):
        new_expense = {
            'id': expenses_df.id.max() + 1,
            'date': spending_date,
            'description': description,
            'category': selected_catego,
            'sub_category': sub_category,
            'amount': amount
        }

        expenses_df = read_csv_from_gcs(f'{USER_DEPENSES}_expenses.csv', bucket_name=BUCKET_NAME)
        expenses_df.loc[len(expenses_df)] = new_expense
        write_csv_to_gcs(expenses_df, f'{USER_DEPENSES}_expenses.csv', bucket_name=BUCKET_NAME)
        st.success("Expense added successfully!")


# Define a function to add new expenses
def add_recette():
    # st.header("Add New recettes")

    # Form inputs for adding a new expense
    recette_date = st.date_input("Date")
    description = st.text_input("Description")
    category = st.selectbox("Select Category", CATEGORIES['recettes'])
    amount = st.number_input("Amount", min_value=0.01)

    # Add the new expense to the database
    if st.button("Add recette"):
        recettes_df = read_csv_from_gcs(f'{USER_DEPENSES}_recettes.csv')
        new_expense = {
            'id': recettes_df.id.max() + 1,
            'date': recette_date,
            'description': description,
            'category': category,
            'amount': amount
        }
        
        recettes_df.loc[len(recettes_df)] = new_expense
        write_csv_to_gcs(recettes_df, f'{USER_DEPENSES}_recettes.csv')

        st.success("Expense added successfully!")


# Define a function to view and delete expenses
def view_and_delete_db(table_name):
    csv_filename = f'{USER_DEPENSES}_{table_name}.csv'
    data_df = read_csv_from_gcs(csv_filename)
    if len(data_df) > 0:
        data_to_delete = st.multiselect(f"Select {table_name} to delete", list(data_df.id.unique()))
        if st.button(f"Delete Selected {table_name}"):
            with_deletion_data_df = data_df[~data_df.id.isin(data_to_delete)]
            write_csv_to_gcs(with_deletion_data_df, csv_filename)
            data_df = read_csv_from_gcs(csv_filename)
        st.table(data_df)

    else:
        st.info(f"No {table_name} recorded yet.")