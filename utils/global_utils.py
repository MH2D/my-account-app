import streamlit as st
import sqlite3
import json
from pathlib import Path
import pandas as pd
import plotly.graph_objs as go
import colorsys
import seaborn as sns
import numpy as np


DATA_PATH = Path('data')
DB_NAME = 'account_management.db'
with open(DATA_PATH / 'categories.json', 'r') as json_file:
    CATEGORIES = json.load(json_file)

def start_db(db_name, DATA_PATH):
    CONN = sqlite3.connect(DATA_PATH / db_name)
    CURSOR = CONN.cursor()
    return CONN, CURSOR



def get_df_from_table(CONN, CURSOR, table_name, return_table_data=False):
    # Fetch column names from the database table
    CURSOR.execute(f"PRAGMA table_info({table_name})")
    column_data = CURSOR.fetchall()
    id_to_col_names = {col[0]: col[1] for col in column_data}

    # Fetch all expenses from the database
    CURSOR.execute(f"SELECT * FROM {table_name}")
    table_data = CURSOR.fetchall()
    table_df = pd.DataFrame(table_data, columns=id_to_col_names.values())
    table_df.date = pd.to_datetime(table_df.date, format='%Y-%m-%d')
    table_df = table_df.sort_values(by=['date'])

    if return_table_data:
        return table_data, table_df
    else:
        return table_df


# Convert RGB tuple to hexadecimal color code
def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
def hex_to_RGB(hex_str):
    """ #FFFFFF -> [255,255,255]"""
    #Pass 16 to the integer function for change of base
    return [int(hex_str[i:i+2], 16) for i in range(1,6,2)]

def get_color_gradient(c1, c2, n):
    """
    Given two hex colors, returns a color gradient
    with n colors.
    """
    c1_rgb = np.array(hex_to_RGB(c1))/255
    c2_rgb = np.array(hex_to_RGB(c2))/255
    mix_pcts = [(x+1)/(n+1) for x in range(n)]
    rgb_colors = [((1-mix)*c1_rgb + (mix*c2_rgb)) for mix in mix_pcts]
    return ["#" + "".join([format(int(round(val*255)), "02x") for val in item]) for item in rgb_colors]

def callback():
    st.session_state.button_clicked = True