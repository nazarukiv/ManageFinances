import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

st.set_page_config(page_title="Manage my finances", page_icon="💷", layout="wide")


def load_transactions(uploaded_file):
    pass


def main():
    st.title("My Finances Dashboard")
    uploaded_file = st.file_uploader("Upload your transaction CSV file", type = ['cvs'])

    if uploaded_file is not None:
        df = load_transactions(uploaded_file)


main()
