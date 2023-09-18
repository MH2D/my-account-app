import streamlit as st
from utils.my_variables import *
from utils.global_utils import *
from utils.expense_recettes_manage import *
from utils.first_dashboard import *



# Main function to switch between pages
def main(USERNAME):
    st.title("Daily Spendings App")

    # Create a navigation menu
    page = st.sidebar.selectbox("Select a page", ["Expenses", "Recettes", "Dashboard"])

    if page == "Expenses":
        add_tab, modif_tab = st.tabs(['Add new', 'Manage'])
        with add_tab:
            add_expense(USERNAME)

        with modif_tab:
            view_and_delete_db(table_name='expenses', USERNAME=USERNAME)



    if page == "Recettes":
        add_tab, modif_tab = st.tabs(['Add new', 'Manage'])
        with add_tab:
            add_recette(USERNAME)
        
        with modif_tab:
            view_and_delete_db(table_name='recettes', USERNAME=USERNAME)

    if page == "Dashboard":
        balance, expense_analysis = st.tabs(['Expense/Recette balance', 'Expense analysis'])
        with balance:
            do_monthly_balance(USERNAME)
            
        
        with expense_analysis:
            do_altair_overall(USERNAME)
            plot_current_month(USERNAME)
            pass
