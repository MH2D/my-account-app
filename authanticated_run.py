import streamlit as st
from utils.my_variables import *
from utils.global_utils import *
from utils.expense_recettes_manage import *
from utils.first_dashboard import *
from utils.mes_limites_depenses import *


def main(USERNAME):
    st.title("Daily Spendings App")

    # Create a navigation menu
    page = st.sidebar.selectbox("Select a page", ["Dashboard", "Expenses", "Recettes", "My preferences"])

    if page == "Dashboard":
        limit_page, balance, expense_analysis = st.tabs(["This month's goals", 'Savings over time', 'Expense TS analysis'])
        with limit_page:
            plot_budget_actual_limits(USERNAME)
        
        with balance:
            do_monthly_balance(USERNAME)
            
        
        with expense_analysis:
            do_altair_overall(USERNAME)
            plot_current_month(USERNAME)
            pass


    if page == "Expenses":
        add_tab, from_csv, modif_tab = st.tabs(['Add new', 'Add from CSV', 'Manage'])

        with add_tab:
            add_expense(USERNAME)

        with from_csv:
            read_file_expenses(USERNAME)
            
        with modif_tab:
            view_and_delete_db(table_name='expenses', USERNAME=USERNAME)



    if page == "Recettes":
        add_tab, modif_tab = st.tabs(['Add new', 'Manage'])
        with add_tab:
            add_recette(USERNAME)
        
        with modif_tab:
            view_and_delete_db(table_name='recettes', USERNAME=USERNAME)


    if page == 'My preferences':
        questionnaire_category(USERNAME)