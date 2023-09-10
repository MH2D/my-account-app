import streamlit as st
from utils.global_utils import (
    DATA_PATH,
    CATEGORIES,
    DB_NAME,
    start_db,
    save_and_close_db
)

from utils.expense_recettes_manage import (
    add_expense,
    add_recette,
    view_and_delete_db
)
from utils.first_dashboard import (
    do_altair_overall,
    plot_current_month
)






# Main function to switch between pages
def main():
    st.title("Daily Spendings App")

    # Create a navigation menu
    page = st.sidebar.selectbox("Select a page", ["Expenses", "Recettes", "Dashboard"])

    if page == "Expenses":
        add_tab, modif_tab = st.tabs(['Add new', 'Manage'])
        with add_tab:
            add_expense()

        with modif_tab:
            view_and_delete_db(table_name='expenses')


    if page == "Recettes":
        add_tab, modif_tab = st.tabs(['Add new', 'Manage'])
        with add_tab:
            add_recette()
        
        with modif_tab:
            view_and_delete_db(table_name='recettes')

    if page == "Dashboard":
        overall, my_other = st.tabs(['Overall', 'My other'])
        with overall:
            do_altair_overall()
            plot_current_month()
        
        with my_other:
            # view_and_delete_db(table_name='recettes')
            pass



if __name__ == '__main__':
    main()
