import streamlit as st
import pandas as pd
from utils.my_variables import *
from datetime import date
from utils.global_utils import *
import plotly.express as px
import plotly.graph_objects as go


def questionnaire_category(USERNAME):
    category_list = list(CATEGORIES['expenses'].keys())
    limits_df = read_csv_from_gcs(f'{USERNAME}_budget_limits.csv', bucket_name=BUCKET_NAME)
    if len(limits_df):
        limits_df['category'] = category_list
        limits_df['limit'] = 5

    limit_categories = {}
    for cat in category_list:
        limit_categories[cat] = st.number_input(
            cat,
            value=limits_df[limits_df.category == cat].values[0],
            min_value=5
            )
        
    if st.button('Update your budget limits'):
        st.write(limit_categories)
        for cat, lim in limit_categories.items():
            limits_df.limit = limits_df.category.apply(lambda x: limit_categories[x])

        write_csv_to_gcs(limits_df, f'{USERNAME}_budget_limits.csv', bucket_name=BUCKET_NAME)

    st.table(limits_df)
    
def plot_budget_actual_limits(USERNAME):

    limits_df = read_csv_from_gcs(f'{USERNAME}_budget_limits.csv', bucket_name=BUCKET_NAME)
    expenses_df, _ = get_expenses_recettes(USERNAME)
    
    this_month_expenses = expenses_df.sort_index()[date.today().replace(day=1).strftime(FRENCH_DATEFORMAT):].copy()
    this_month_expenses = this_month_expenses.groupby('category').agg({'amount':'sum'})
    limits_and_expenses_for_plot = pd.merge(limits_df, this_month_expenses, right_index=True, left_on='category', how='outer').fillna(0)

    limits_and_expenses_for_plot['limit_reached'] = limits_and_expenses_for_plot.amount / limits_and_expenses_for_plot.limit
    limits_and_expenses_for_plot['available_budget'] = limits_and_expenses_for_plot.limit - limits_and_expenses_for_plot.amount

    limits_and_expenses_for_plot['limit_text']= limits_and_expenses_for_plot.limit.apply(lambda x: f'Limit: {x:.0f}€')
    limits_and_expenses_for_plot['avail_budg_text']= limits_and_expenses_for_plot.available_budget.apply(
        lambda x: f'Left: {x:.0f}€' if x > 0 else 'Nothing left !'
        )
    # THE PLOT

    # Define a color scale (green to red)
    color_scale = ['#008000', '#FFFF00', '#FF0000']  # Green, Yellow, Red
    # Create a color map based on percent values
    color_map = np.interp(limits_and_expenses_for_plot.limit_reached, [0, 1], [0, 2])
    bar_colors = [color_scale[int(value)] for value in color_map]



    fig = go.Figure()
    # Add a bar trace
    proportion_bar = go.Bar(
        x=limits_and_expenses_for_plot.limit_reached,
        y=limits_and_expenses_for_plot.category,
        name='\% Limit reached',
        orientation='h',
        text=limits_and_expenses_for_plot.avail_budg_text,
        textposition='inside',
        marker=dict(color=bar_colors),
        showlegend=False
    )

    limit_bar = go.Bar(
        x=limits_and_expenses_for_plot.limit / limits_and_expenses_for_plot.limit,
        y=limits_and_expenses_for_plot.category,
        orientation='h',
        text=limits_and_expenses_for_plot.limit_text,
        textposition='outside',
        marker=dict(color='rgba(0,0,0,0)', line=dict(color='black', width=2)),
        showlegend=False
    )

    # Add both traces to the subplot
    fig.add_trace(proportion_bar)
    fig.add_trace(limit_bar)

    # Customize the layout
    fig.update_layout(
        title='Budget limits',
        xaxis=dict(title=''),  # Adjust the x-axis title
        yaxis=dict(title=''),
        barmode='overlay'  # Overlay the bars for the same category
    )
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)

    st.plotly_chart(fig, use_container_width=True)







