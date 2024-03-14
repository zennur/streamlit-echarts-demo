import streamlit as st
import pandas as pd
import plotly.express as px

# Title of the app
st.title("Data Visualization App for Product Owners")

# File uploader widget
uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx'])

if uploaded_file is not None:
    # Read the uploaded file
    if uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(uploaded_file)

    # Display the dataframe
    st.write("Data Preview:", df.head())

    # Column selection for visualization
    columns = df.columns.tolist()
    selected_columns = st.multiselect("Select columns to visualize", columns, default=columns[:2])

    # Choosing a plot type
    plot_type = st.selectbox("Select the type of plot", ["Line", "Bar", "Scatter", "Heatmap", "Time Series"])

    # Plotting based on the selected options
    if st.button("Generate Plot"):
        if plot_type == "Line":
            fig = px.line(df, x=selected_columns[0], y=selected_columns[1:])
        elif plot_type == "Bar":
            fig = px.bar(df, x=selected_columns[0], y=selected_columns[1:])
        elif plot_type == "Scatter":
            fig = px.scatter(df, x=selected_columns[0], y=selected_columns[1])
        # Heatmap option
        elif plot_type == "Heatmap":
            fig = px.imshow(df[selected_columns].corr())
            st.plotly_chart(fig)
        # Convert column to datetime if necessary
        # df['Your Date Column'] = pd.to_datetime(df['Your Date Column'])
        elif plot_type == "Time Series":
            time_column = st.selectbox("Select the time column", options=selected_columns)
            df[time_column] = pd.to_datetime(df[time_column], unit='us')
            # value_column = st.selectbox("Select the value column", options=[col for col in selected_columns if col != time_column])
            value_columns = [x for x in selected_columns if x != time_column]
            fig = px.line(df, x=time_column, y=value_columns, title='Time Series Plot')
            st.plotly_chart(fig)



        st.plotly_chart(fig)

# Instructions or user guide
st.sidebar.header("Instructions")
st.sidebar.text("1. Upload your CSV or Excel file.")
st.sidebar.text("2. Select the columns to visualize.")
st.sidebar.text("3. Choose the type of plot.")
st.sidebar.text("4. Click on 'Generate Plot' to visualize.")
