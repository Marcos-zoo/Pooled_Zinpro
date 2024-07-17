import streamlit as st
import pandas as pd
#from streamlit_option_menu import option_menu
import plotly.express as px


def zinc_chrome_cumulative():
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
    def load_data_cumulative():
        # Load the data from an Excel file
        df3 = pd.read_excel("Europe_analysis_pool_2.xlsx", sheet_name='CUMULATIVE', na_values='NaN')
        df4 = pd.read_excel("Europe_analysis_pool_2.xlsx", sheet_name='P_cumulative')
        return df3, df4

    # Load the data
    df3, df4 = load_data_cumulative()

    # Define the color map
    color_map = {'IM': '#000000', 'Availa-iso': '#000061'}

    def graphs_performance_cumulative():
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
        st.markdown('<h2 class="center-text">Cumulative performance</h2>', unsafe_allow_html=True)

        # Map treatment codes to names
        df3['TR'] = df3['TR'].map({1: 'IM', 2: 'Availa-iso'})

        # Aggregate the data to get the mean for each treatment
        aggregated_data = df3.groupby('TR', as_index=False).mean().round(3)

        # Display the mean values grouped by treatment
        st.write("Average Values by Treatment")
        st.dataframe(aggregated_data)

        # Create columns for the plots
        col1, col2 = st.columns(2)

        # Track the current column for plotting
        current_column = col1

        for idx, col_name in enumerate(df3.columns[1:]):
            # Ensure df4 has the column before proceeding
            if col_name in df4.columns:
                # Plot using Plotly
                y = col_name
                error_y = df3.groupby('TR')[y].std()

                fig = px.bar(aggregated_data, x='TR', y=y, title=col_name,
                             color='TR', color_discrete_map=color_map,
                             category_orders={'TR': ['IM', 'Availa-iso']},
                             error_y=error_y)

                fig.update_layout(
                    template="plotly_white",
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    yaxis=dict(
                        showgrid=False,  # Hide horizontal grid lines
                        range=[df3[y].min() * 0.9, df3[y].max() + df3[y].std()]
                        # Set the range of the Y-axis
                    )
                )

                p_value = df4.loc[0, y]
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

    graphs_performance_cumulative()
