import streamlit as st
import pandas as pd
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
        CONN, CURSOR = start_db(DB_NAME, DATA_PATH=DATA_PATH)
        CURSOR.execute('''
        INSERT INTO expenses (
            date, description, category, sub_category, amount
            ) VALUES (?, ?, ?, ?, ?)''',
                        (spending_date, description, selected_catego, sub_category, amount))
        CONN.commit()
        st.success("Expense added successfully!")

        CONN.close()

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
        CONN, CURSOR = start_db(DB_NAME, DATA_PATH=DATA_PATH)

        CURSOR.execute('''
        INSERT INTO recettes (
            date, description, category, amount
            ) VALUES (?, ?, ?, ?)''',
                        (recette_date, description, category, amount))
        CONN.commit()
        st.success("Expense added successfully!")
        CONN.close()


# Define a function to view and delete expenses
def view_and_delete_db(table_name):
    st.header("View Expenses and Delete")
    CONN, CURSOR = start_db(DB_NAME, DATA_PATH=DATA_PATH)

    table_data, table_df = get_df_from_table(CONN, CURSOR, table_name, return_table_data=True)
    
    if table_data:

        # Delete
        data_to_delete = st.multiselect(f"Select {table_name} to delete", [data[0] for data in table_data])
        if st.button(f"Delete Selected {table_name}"):
            for data_id in data_to_delete:
                CURSOR.execute(f"DELETE FROM {table_name} WHERE id=?", (data_id,))
            CONN.commit()
            st.success(f"Selected {table_name} deleted successfully.")
        st.table(table_df)

        # Modify

        # editable_df = st.data_editor(table_df, disabled='id')

        # # Save changes if "Save" button is clicked
        # if st.button("Save Changes"):
        #     changed_index = editable_df.compare(table_df, align_axis = 0).reset_index().level_0.unique()
        #     st.table(editable_df.compare(table_df, align_axis = 0).reset_index())
        #     # Validate and update changes
        #     # You can implement your validation rules here
        #     update_table(editable_df.iloc[changed_index], table_name, id_to_col_names, CONN, CURSOR)
        #     st.text('bjr')
        #     st.success("Changes saved!")

    else:
        st.info(f"No {table_name} recorded yet.")
    CONN.close()


def update_table(updated_data, table_name, id_to_col_names, conn, cursor):
    for _, row in updated_data.iterrows():
        str_for_query = ', '.join([f'{val} = ?' for val in list(id_to_col_names.values())[1:]])
        tuple_values = tuple([row[val] for val in id_to_col_names.values()])
        st.text(tuple_values)

        query = f"UPDATE {table_name} SET {str_for_query} WHERE id = ?"
        cursor.execute(query, tuple_values)
    conn.commit()