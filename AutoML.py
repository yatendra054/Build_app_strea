import streamlit as st
import pandas as pd
import os
from ydata_profiling import ProfileReport
from streamlit_ydata_profiling import st_profile_report
from pycaret.regression import setup, compare_models, save_model, pull

with st.sidebar:
    st.image("AutoML.png")
    st.title("Auto ML")
    choice = st.radio("# Navigation", ["Upload:bookmark_tabs:", "Profiling", "AutoMl", "Downloading:arrow_down:"])
    st.info("This application is used to design auto machine learning model by uploading data")

if os.path.exists("dataset.xlsx"):
    if "dataset.xlsv".endswith('.csv'):
        df= pd.read_csv("dataset.xlsv", index_col=None)
    elif "dataset.xlsx".endswith('.xlsx'):
        df = pd.read_csv("dataset.xlsx", index_col=None)

if choice == "Upload:bookmark_tabs:":
    st.title("Uploading Your Data for Auto Modelling!")
    file = st.file_uploader("Upload Your Dataset")
    if file is not None:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file,index_col=None)
        elif file.name.endswith('.xlsv'):
            df = pd.read_excel(file, index_col=None)

        if file.name.endswith('.csv'):
            df.to_csv("dataset.csv", index=None)
        elif file.name.endswith('.xlsv'):
            df.to_csv("dataset.xlsx", index=None)
        st.dataframe(df)

if choice == "Profiling":
    if df is not None:
        st.title("Automated exploratory analysis of data")
        profile_report = ProfileReport(df, explorative=True, correlations=None)
        st_profile_report(profile_report)
if choice == "AutoMl":
    if st.button("Train Model"):
        st.title("Automated Machine Learning**")
        target = st.selectbox("Select your Target", df.columns)
        setup(df, target=target)
        setup_df = pull()
        st.info("This is a ML experiment system")
        st.dataframe(setup_df)
        best_model = compare_models()
        compare_df = pull()
        st.info("This is a Ml model")
        st.dataframe(compare_df)
        save_model(best_model, "best_model.pkl")

if choice == "Downloading:arrow_down:":
    with open("best_model.pkl", "rb") as f:
        st.download_button("Download Model", f, "train_model.pkl")