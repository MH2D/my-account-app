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

def do_altair_overall(USERNAME): 
    # Over time and category
    expense_df, _ = get_expenses_recettes(USERNAME)

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


def plot_current_month(USERNAME):
    
    expense_df, recettes_df = get_expenses_recettes(USERNAME)
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


def do_monthly_balance(USERNAME): 
    # Over time and category
    expense_df, recettes_df = get_expenses_recettes(USERNAME)
    expense_df.head()

    expense_df.amount = - expense_df.amount

    total_df = pd.concat([expense_df[['amount']], recettes_df[['amount']]])

    total_df = total_df.groupby(
        [
            pd.Grouper(freq=f'1m')
        ]
        )['amount'].sum().reset_index()

    total_df.date = total_df['date'].dt.strftime('%B %Y')
    total_df['cumsum'] = total_df.amount.cumsum()

    fig = go.Figure(go.Waterfall(
        orientation = "v",
        x = total_df.date,
        textposition = "outside",
        text = total_df.amount.round().astype(str).values,
        y = total_df.amount,
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
    ))

    fig.update_layout(
            title = "Waterfall chart",
            yaxis_range= [np.min([-10,total_df['cumsum'].min()*1.1]), np.max([10, total_df['cumsum'].max()*1.1])]

    )

    st.plotly_chart(fig, use_container_width=True)