import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objs as go
import colorsys
import seaborn as sns
import datetime as dt
from utils.my_variables import *
from utils.global_utils import *

expense_df =  read_csv_from_gcs(f'{USER_DEPENSES}_expenses.csv')
expense_df = expense_df.set_index('date')
expense_df.index = pd.to_datetime(expense_df.index, format=FRENCH_DATEFORMAT)

recettes_df =  read_csv_from_gcs(f'{USER_DEPENSES}_recettes.csv')
recettes_df = recettes_df.set_index('date')
recettes_df.index = pd.to_datetime(recettes_df.index, format=FRENCH_DATEFORMAT)


def do_altair_overall(): 
    expense_df =  read_csv_from_gcs(f'{USER_DEPENSES}_expenses.csv')
    expense_df = expense_df.set_index('date')
    expense_df.index = pd.to_datetime(expense_df.index, format=FRENCH_DATEFORMAT)

    recettes_df =  read_csv_from_gcs(f'{USER_DEPENSES}_recettes.csv')
    recettes_df = recettes_df.set_index('date')
    recettes_df.index = pd.to_datetime(recettes_df.index, format=FRENCH_DATEFORMAT)

    # Over time and category
    st.subheader("Expense over time")
    freq_to_name = {
        'Month': 'm',
        'Year': 'y',
        'Day': 'd',
    }

    col1, col2 = st.columns(2)
    selected = col1.selectbox('Select the window step', list(freq_to_name.keys()))
    size_window = col2.number_input('Select the window size', min_value=1, step=1)

    monthly_cat_exp = expense_df.groupby(
        [
            pd.Grouper(freq=f'{size_window}{freq_to_name[selected]}'),
        'category'
        ]
        )['amount'].sum().reset_index()

    plot_bar_time = px.bar(
        monthly_cat_exp,
        x='date',
        y='amount',
        color='category',
        title=f'Over time expenses. Window: {size_window} {selected}'
        )
    st.plotly_chart(plot_bar_time, use_container_width=True)


def plot_current_month():
    expense_df =  read_csv_from_gcs(f'{USER_DEPENSES}_expenses.csv')
    expense_df = expense_df.set_index('date')
    expense_df.index = pd.to_datetime(expense_df.index, format=FRENCH_DATEFORMAT)

    recettes_df =  read_csv_from_gcs(f'{USER_DEPENSES}_recettes.csv')
    recettes_df = recettes_df.set_index('date')
    recettes_df.index = pd.to_datetime(recettes_df.index, format=FRENCH_DATEFORMAT)

    st.subheader("Monthly breakdown")

    current_month = st.date_input("Date")
    this_month_data = expense_df[
        (expense_df.index.month == current_month.month) &
        (expense_df.index.year == current_month.year)

    ].copy()
    inner_donut_data = this_month_data.groupby('category')['amount'].sum().reset_index().sort_values(by='category', ascending=False)
    outer_donut_data = this_month_data.groupby(['category','sub_category'])['amount'].sum().reset_index().sort_values(by=['category', 'amount'], ascending=False)
    sub_cats_number = outer_donut_data.groupby('category').sub_category.count()
    inner_donut_data['color'] = inner_donut_data.category.apply(
        lambda x: CATEGORIES['primal_colors'][x][0]
    )
    all_cols = []
    for catego in outer_donut_data.category.unique():
        all_cols.extend(
            get_color_gradient(
            CATEGORIES['primal_colors'][catego][0], 
            CATEGORIES['primal_colors'][catego][1],
            sub_cats_number[catego]
            )
        )
    outer_donut_data['color'] = all_cols    

    #https://community.plotly.com/t/linking-traces-in-nested-pie-chart-for-legend-toggle-functionality/15433
    data = [# Portfolio (inner donut)
            go.Pie(values=inner_donut_data.amount.values,
                labels=inner_donut_data.category.values,
                domain={'x':[0.2,0.8], 'y':[0.1,0.9]},
                hole=0.5,
                direction='clockwise',
                sort=False,
                marker={'colors':inner_donut_data.color.values}
                ),
            # Individual components (outer donut)
            go.Pie(values=outer_donut_data.amount.values,
                labels=outer_donut_data.sub_category.values,
                domain={'x':[0.1,0.9], 'y':[0,1]},
                hole=0.75,
                direction='clockwise',
                sort=False,
                marker={'colors':outer_donut_data.color.values},
                showlegend=False)]
    
    nested_pie_this_month = go.Figure(data=data, layout={'title':'This month breakdown'})
    # nested_pie_this_month.update_traces(
    #         hovermode='x unified'
    #         )
    st.plotly_chart(nested_pie_this_month, use_container_width=True)
