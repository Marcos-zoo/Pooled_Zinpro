import streamlit as st
import pandas as pd
import plotly.express as px

def age():
    with st.container():
        st.markdown(
            """
            <style>
            .fixed-title {
                position: fixed;
                top: 0;
                width: 100%;
                background-color: white;
                z-index: 9999;
                padding: 30px 0;
                border-bottom: 1px solid #ddd;
            }
            .content {
                margin-top: 10px; /* Adjust this value to add more space below the title */
            }
            .header {
                color: #00009e;
                font-size: 4em;
                font-weight: bold;
                text-align: left;
            }
            .subheader {
                color: #000000;
                font-size: 1.5em;
                font-weight: bold;
                text-align: left;
            }
            .center-text {
                text-align: center;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Fixed title
        st.markdown(
            '<div class="fixed-title"><h1 class="header">Zinc and Chrome Study</h1><h2 class="subheader">Mixed effects</h2></div>',
            unsafe_allow_html=True)

        # Main content with scrollbar
        st.markdown('<div class="content">', unsafe_allow_html=True)


    @st.cache_data
    def load_data():
        # Load the data from an Excel file
        df = pd.read_excel("Europe_analysis_pool_2.xlsx", sheet_name='AGE', na_values='NaN')
        df2 = pd.read_excel("Europe_analysis_pool_2.xlsx", sheet_name='P-VALUES')

        return df, df2

    # Load the data
    df, df2 = load_data()

    # Define the color map
    color_map = {'IM': '#000000', 'Availa-iso': '#000061'}

    # Sidebar for selecting age
    st.sidebar.header('Select period')

    # Define the age options and corresponding number ranges
    age_options = {
        '1 to 7': range(1, 8),
        '14 to 21': range(14, 22),
        '22 to 42': range(22, 43)
    }

    # Create a selectbox with the textual ranges
    selected_range = st.sidebar.selectbox('Select Age', list(age_options.keys()))
    number_range = age_options[selected_range]

    # Display the selected range
    st.write(f"Selected Age Range: {selected_range}")

    def phases():
        if selected_range == '1 to 7':
            st.markdown('<h2 class="left-text">1 to 7 days</h2>', unsafe_allow_html=True)
        elif selected_range == '14 to 21':
            st.markdown('<h2 class="left-text">14 to 21 days</h2>', unsafe_allow_html=True)
        elif selected_range == '22 to 42':
            st.markdown('<h2 class="left-text">22 to 42 days</h2>', unsafe_allow_html=True)

    def graphs_performance():
        st.markdown(
            """
            <style>
            .center-text {
                text-align: center;
                margin-top: 30px; /* Adjust this value as needed */
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Use the custom CSS class to center the subheader
        st.markdown('<h2 class="center-text">Performance by phase</h2>', unsafe_allow_html=True)
        phases()

        # Filter the dataframe based on the number range
        age_filtered = df[df['Age'].isin(number_range)]

        # Map treatment codes to names
        age_filtered['TR'] = age_filtered['TR'].map({1: 'IM', 2: 'Availa-iso'})

        # Aggregate the data to get the mean for each treatment
        aggregated_data = age_filtered.groupby('TR', as_index=False).mean().round(3)

        # Drop the 'Age' column from the aggregated data
        aggregated_data_no_age = aggregated_data.drop(columns=['Age'])

        # Display the mean values grouped by treatment
        st.write("Average Values by Treatment")
        st.dataframe(aggregated_data_no_age)

        # Create columns for the plots
        col1, col2 = st.columns(2)

        # Track the current column for plotting
        current_column = col1

        for idx, col_name in enumerate(df.columns[1:]):
            # Ensure df2 has the column before proceeding
            if col_name in df2.columns:
                # Plot using Plotly
                y = col_name
                age_p = df2[df2['Age'].isin(number_range)].loc[:, y].round(3)
                error_y = age_filtered.groupby('TR')[y].std()

                fig = px.bar(aggregated_data_no_age, x='TR', y=y, title=col_name,
                             color='TR', color_discrete_map=color_map,
                             category_orders={'TR': ['IM', 'Availa-iso', 'Availa-high']},
                             error_y=error_y)

                fig.update_layout(
                    template="plotly_white",
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    yaxis=dict(
                        showgrid=False,  # Hide horizontal grid lines
                        range=[age_filtered[y].min() * 0.9, age_filtered[y].max() + age_filtered[y].std()]
                        # Set the range of the Y-axis
                    )
                )

                p_value = age_p.iloc[0]
                annotation_text = "<i>P</i> < 0.001" if p_value < 0.001 else f"<i>P</i> = {p_value}"

                fig.add_annotation(
                    text=annotation_text,
                    xref="paper", yref="paper",
                    x=1, y=1.05,  # Position it in the upper right corner
                    showarrow=False,
                    font=dict(
                        size=14,
                        color="black"
                    ),
                    align="right"
                )

                # Alternate between columns for each chart
                if current_column == col1:
                    col1.plotly_chart(fig)
                    current_column = col2
                else:
                    col2.plotly_chart(fig)
                    current_column = col1

    graphs_performance()

age()
