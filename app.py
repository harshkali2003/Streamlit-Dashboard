import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Title of the Dashboard
st.title("Streamlit Dashboard Challenge")

# Upload Dataset
uploaded_file = st.file_uploader("Upload your dataset (CSV file)", type=["csv"])
if uploaded_file is not None:
    # Read the uploaded CSV file
    data = pd.read_csv(uploaded_file)

    # Display the first few rows
    st.subheader("Dataset Preview")
    st.write(data.head())

    # Display basic information
    st.subheader("Dataset Summary")
    st.write(data.describe())

    # Sidebar Filters
    st.sidebar.header("Filter Options")
    numeric_columns = data.select_dtypes(include=np.number).columns.tolist()
    
    # Filter based on a selected numeric column
    if numeric_columns:
        selected_column = st.sidebar.selectbox("Select a column to filter by", numeric_columns)
        min_value, max_value = data[selected_column].min(), data[selected_column].max()
        selected_range = st.sidebar.slider(f"Select range for {selected_column}", min_value, max_value, (min_value, max_value))
        filtered_data = data[(data[selected_column] >= selected_range[0]) & (data[selected_column] <= selected_range[1])]
        st.subheader(f"Filtered Data by {selected_column}")
        st.write(filtered_data)

    # Plot Visualizations
    st.subheader("Visualizations")
    plot_type = st.selectbox("Select plot type", ["Histogram", "Scatter Plot", "Correlation Heatmap"])

    if plot_type == "Histogram":
        column = st.selectbox("Select a column for Histogram", numeric_columns)
        st.write(f"Histogram for {column}")
        fig, ax = plt.subplots()
        sns.histplot(filtered_data[column], kde=True, ax=ax)
        st.pyplot(fig)

    elif plot_type == "Scatter Plot":
        col1, col2 = st.columns(2)
        x_axis = col1.selectbox("X-axis", numeric_columns)
        y_axis = col2.selectbox("Y-axis", numeric_columns)
        st.write(f"Scatter Plot: {x_axis} vs {y_axis}")
        fig, ax = plt.subplots()
        sns.scatterplot(data=filtered_data, x=x_axis, y=y_axis, ax=ax)
        st.pyplot(fig)

    elif plot_type == "Correlation Heatmap":
        st.write("Correlation Heatmap")
        fig, ax = plt.subplots()
        sns.heatmap(filtered_data.corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

else:
    st.warning("Please upload a CSV file to proceed.")
