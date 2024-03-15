import streamlit as st
import sqlite3
import json
from pathlib import Path
import pandas as pd
import plotly.graph_objs as go
import colorsys
import seaborn as sns
import numpy as np
from google.cloud import storage
from io import BytesIO
from utils.my_variables import *


def read_csv_from_gcs(csv_filename, bucket_name=BUCKET_NAME):
    # Get the bucket
    bucket = CLIENT.get_bucket(bucket_name)

    try:
        # Get the blob (object) corresponding to the SQLite database file
        blob = bucket.blob(csv_filename)

        # Read the CSV file directly into a DataFrame
        content = blob.download_as_string()
        csv_df = pd.read_csv(BytesIO(content))
        date1 = pd.to_datetime(csv_df['date'], errors='coerce', format='%Y-%m-%d')
        date2 = pd.to_datetime(csv_df['date'], errors='coerce', format='%d-%m-%Y')
        csv_df['date'] = date1.fillna(date2)
        
    except:
        if 'expenses' in csv_filename:
            cols = ['id', 'date', 'description', 'libelle_banque', 'category', 'sub_category', 'amount']
        elif 'recette' in csv_filename:
            cols = ['id', 'date', 'description', 'libelle_banque', 'category', 'amount']
        elif 'budget_limits' in csv_filename:
            cols = ['category', 'limit']
        
        csv_df = pd.DataFrame(columns=cols)

    return csv_df

def write_csv_to_gcs(to_save_df, saved_filename, bucket_name=BUCKET_NAME):
    
    csv_content = to_save_df.to_csv(index=False)
    
    # Define the blob (object) to write
    bucket = CLIENT.get_bucket(bucket_name)

    # Define the blob (object) to write
    blob = bucket.blob(saved_filename)

    # Upload the CSV content to GCS
    blob.upload_from_string(csv_content, content_type='text/csv')


def get_expenses_recettes(USERNAME):
    expense_df =  read_csv_from_gcs(f'{USERNAME}_expenses.csv')
    expense_df = expense_df.set_index('date').sort_index()
    expense_df.index = pd.to_datetime(expense_df.index, format=FRENCH_DATEFORMAT)

    recettes_df =  read_csv_from_gcs(f'{USERNAME}_recettes.csv')
    recettes_df = recettes_df.set_index('date').sort_index()
    recettes_df.index = pd.to_datetime(recettes_df.index, format=FRENCH_DATEFORMAT)
    return expense_df, recettes_df


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