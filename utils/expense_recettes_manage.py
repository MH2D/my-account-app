import streamlit as st
import pandas as pd
from utils.my_variables import *

from utils.global_utils import *

def new_EXPENSE_exp_to_db(USERNAME, spending_date, description, category, sub_category, amount, libelle='Not mentioned'):
    expenses_df = read_csv_from_gcs(f'{USERNAME}_expenses.csv', bucket_name=BUCKET_NAME)
    new_id = expenses_df.id.max() + 1
    if np.isnan(new_id):
        new_id = 1

    new_expense = {
        'id': new_id,
        'date': spending_date,
        'description': description,
        'libelle_banque': libelle,
        'category': category,
        'sub_category': sub_category,
        'amount': amount
    }

    expenses_df.loc[len(expenses_df)] = new_expense
    write_csv_to_gcs(expenses_df, f'{USERNAME}_expenses.csv', bucket_name=BUCKET_NAME)
    
def new_RECETTE_exp_to_db(USERNAME, spending_date, description, category, amount, libelle='Not mentioned'):
    recettes_df = read_csv_from_gcs(f'{USERNAME}_recettes.csv')
    new_id = recettes_df.id.max() + 1
    if np.isnan(new_id):
        new_id = 1
        
    new_expense = {
        'id': new_id,
        'date': spending_date,
        'description': description,
        'libelle_banque': libelle,
        'category': category,
        'amount': amount
    }
    
    recettes_df.loc[len(recettes_df)] = new_expense
    write_csv_to_gcs(recettes_df, f'{USERNAME}_recettes.csv')


# Define a function to add new expenses
def add_expense(USERNAME):

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
        new_EXPENSE_exp_to_db(USERNAME, spending_date, description, selected_catego, sub_category, amount)
        st.success("Expense added successfully!")


# Define a function to add new expenses
def add_recette(USERNAME):
    # st.header("Add New recettes")

    # Form inputs for adding a new expense
    recette_date = st.date_input("Date")
    description = st.text_input("Description")
    category = st.selectbox("Select Category", CATEGORIES['recettes'])
    amount = st.number_input("Amount", min_value=0.01)

    # Add the new expense to the database
    if st.button("Add recette"):
        new_RECETTE_exp_to_db(USERNAME, recette_date, description, category, amount)
        st.success("Expense added successfully!")


# Define a function to view and delete expenses
def view_and_delete_db(table_name, USERNAME):
    csv_filename = f'{USERNAME}_{table_name}.csv'
    data_df = read_csv_from_gcs(csv_filename)
    data_df = data_df.sort_values('id', ascending=False)
    if len(data_df) > 0:
        data_to_delete = st.multiselect(f"Select {table_name} to delete", list(data_df.id.unique()))
        if st.button(f"Delete Selected {table_name}"):
            with_deletion_data_df = data_df[~data_df.id.isin(data_to_delete)]
            write_csv_to_gcs(with_deletion_data_df, csv_filename)
            data_df = read_csv_from_gcs(csv_filename)

        st.table(data_df.sort_values('id', ascending=False))

    else:
        st.info(f"No {table_name} recorded yet.")



    
def read_file_expenses(USERNAME):
    # File uploader widget
    if 'index_df' not in st.session_state:
        st.session_state.index_df = 0
    
    if 'disabled' not in st.session_state:
        st.session_state['disabled'] = False
    
    if 'added_rows' not in st.session_state:
        st.session_state['added_rows'] = []

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    

    if uploaded_file is not None:
        st.write(st.session_state.index_df)
        df = read_csv_input_and_filter(USERNAME, uploaded_file)


        current_montant = df.iloc[st.session_state.index_df]["montant"]
        type_of_line = 'EXPENSE' if current_montant < 0 else 'RECETTE'

        st.write(f'Current row: {st.session_state.index_df} over {len(df)}')

        spending_date = st.date_input("Date", value=df.iloc[st.session_state.index_df]["date"])
        description = st.text_input("Description", value=df.iloc[st.session_state.index_df]["description"])
        libelle = df.iloc[st.session_state.index_df]["libelle"]


        if current_montant < 0:
            selected_category = st.selectbox("Select Category", list(CATEGORIES['expenses'].keys()), key=f'catego_{st.session_state.index_df}')
            selected_subcategories = CATEGORIES['expenses'].get(selected_category, [])
            sub_category = st.selectbox("Select Sub Category", selected_subcategories,  key=f'sub_catego_{st.session_state.index_df}')
        
        else:
            selected_category = st.selectbox("Select Category", CATEGORIES['recettes'], key=f'catego_{st.session_state.index_df}')
        
        amount = st.number_input("Amount", value=df.iloc[st.session_state.index_df]["montant"])
        st.write(st.session_state.index_df)

        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            if st.button(f"Add {type_of_line} from csv", disabled=st.session_state['disabled']):
                if type_of_line == 'EXPENSE':
                    new_EXPENSE_exp_to_db(USERNAME, spending_date, description, selected_category, sub_category, amount, libelle=libelle)
                    st.success("Expense added successfully from csv!")
                    st.session_state.added_rows.append(st.session_state.index_df)
                    st.write(st.session_state.index_df) 
                    st.session_state.index_df = st.session_state.index_df + 1

                else:
                    new_RECETTE_exp_to_db(USERNAME, spending_date, description, selected_category, amount, libelle=libelle)
                    st.success("Recette added successfully from csv!")
                    st.session_state.added_rows.append(st.session_state.index_df)
                    st.write(st.session_state.index_df)
                    st.session_state.index_df = st.session_state.index_df + 1

        with col2:
            if st.button("Pass", disabled=st.session_state['disabled']):
                st.session_state.index_df = st.session_state.index_df + 1

        with col3:
            if st.button("Stop and download"):
                    data = df[~df.index.isin(st.session_state.added_rows)].to_csv().encode('latin1')
                    st.download_button("Download remaining rows", data=data, file_name='large_df.csv', mime='text/csv')
                    st.session_state.disabled = True


        if st.session_state.index_df >= len(df):
            st.session_state.disabled = True

        st.write(st.session_state['added_rows'])


def read_csv_input_and_filter(USERNAME, uploaded_file):
    df = pd.read_csv(uploaded_file, sep=',', encoding='latin1').reset_index(drop=True)
    try:
        df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
        df["montant"] = df["montant"].str.replace(',', '.').astype(float)

    except:
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
        df["montant"] = df.montant.astype(float)
        
    df = df.sort_values('date')
    st.write(df.head(4))

    csv_filename = f'{USERNAME}_expenses.csv'
    exp = read_csv_from_gcs(csv_filename)
    st.write(exp.head(4))