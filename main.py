import json
import os.path
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Manage my finances", page_icon="💷", layout="wide")

category_file = "categories.json"

if "categories" not in st.session_state:
    st.session_state.categories = {
        "Uncategorized": []
    }

if os.path.exists(category_file):
    with open(category_file, 'r') as f:
        st.session_state.categories = json.load(f)
else:
    with open(category_file, "w") as f:
        json.dump(st.session_state.categories, f, indent=4)


def save_categories():
    with open(category_file, "w") as f:
        json.dump(st.session_state.categories, f, indent=4)


def categorize_transactions(df):
    df["Category"] = "Uncategorized"
    for category, keywords in st.session_state.categories.items():
        if category == "Uncategorized" or not keywords:
            continue

        lowered_keywords = [keyword.lower().strip() for keyword in keywords]

        for idx, row in df.iterrows():
            reference = str(row["Spending Category"]).lower().strip()
            if any(kw in reference for kw in lowered_keywords):
                df.at[idx, "Category"] = category
                break
    return df


def load_transactions(file):
    try:
        df = pd.read_csv(file)
        df.columns = [col.strip() for col in df.columns]
        df["Amount (GBP)"] = df["Amount (GBP)"].replace(",", "", regex=True).astype(float)
        df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
        df["Date"] = df["Date"].dt.date
        df = categorize_transactions(df)
        st.session_state.df = df
        st.success("File loaded successfully")
        return df
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None


def add_keyword_to_category(category, keyword):
    keyword = keyword.strip()
    if keyword and keyword not in st.session_state.categories[category]:
        st.session_state.categories[category].append(keyword)
        save_categories()
        return True
    return False


def main():
    st.title("💷 My Finances Dashboard")

    uploaded_file = st.file_uploader("📂 Upload your transaction CSV file", type=["csv"])
    if uploaded_file:
        df = load_transactions(uploaded_file)

    st.subheader("➕ Add new category")
    new_category = st.text_input("New category")
    add_button = st.button("Add category")

    if add_button and new_category:
        if new_category not in st.session_state.categories:
            st.session_state.categories[new_category] = []
            save_categories()
            st.success(f"New category added: {new_category}")
            st.rerun()
        else:
            st.warning("Category already exists.")

    if "df" in st.session_state:
        st.subheader("📊 Your categorized expenses")

        selected_category = st.selectbox(
            "Filter by category",
            ["All"] + list(st.session_state.categories.keys())
        )

        df = st.session_state.df

        if selected_category != "All":
            filtered_df = df[df["Category"] == selected_category]
        else:
            filtered_df = df

        edited_df = st.data_editor(
            filtered_df,
            num_rows="dynamic",
            use_container_width=True
        )
        st.session_state.df = edited_df

        st.subheader("📈 Expenses Breakdown by Category")

        expense_df = df[df["Amount (GBP)"] < 0]
        summary = (
            expense_df.groupby("Category")["Amount (GBP)"]
            .sum()
            .abs()
            .sort_values(ascending=False)
        )

        if not summary.empty:
            st.plotly_chart(
                px.pie(
                    names=summary.index,
                    values=summary.values,
                    title="Spending Distribution by Category",
                    hole=0.4
                ),
                use_container_width=True
            )
        else:
            st.info("No expenses available to visualize.")

        st.subheader("📋 Summary of Expenses")
        summary_df = edited_df.groupby("Category")["Amount (GBP)"].sum().reset_index()
        summary_df = summary_df.rename(columns={"Amount (GBP)": "Total (GBP)"})
        summary_df["Total (GBP)"] = summary_df["Total (GBP)"].round(2)
        st.dataframe(summary_df)

        total_expense = summary_df[summary_df["Total (GBP)"] < 0]["Total (GBP)"].sum()
        st.markdown(f"### 💰 **Total Expenses: £{abs(total_expense):,.2f}**")


main()

todo_list = [
    "Multiple file uploads",
    "Authentication layer",
    "Dockerize it",
    "README with GIFs and images",
    "Unit tests",
]