import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Manage my finances", page_icon="💷", layout="wide")


def load_transactions(file):
    try:
        df = pd.read_csv(file)
        df.columns = [col.strip() for col in df.columns]
        df["Amount (GBP)"] = df["Amount (GBP)"].replace(",", "", regex=True).astype(float)
        df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
        df["Date"] = df["Date"].dt.date

        st.write(df)
        return df
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None

def main():
    st.title("my finances dashboard")
    uploaded_file = st.file_uploader("upload your transaction csv file", type=["csv"])
    if uploaded_file:
        df = load_transactions(uploaded_file)


main()