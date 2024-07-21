"""
Created on Fri Jun 21 11:59:31 2024

@author: marco
"""

import streamlit as st
from streamlit_option_menu import option_menu
import age_europa_pooled
import age_europa_pooled_cumulative

st.set_page_config(page_title='Zinpro', page_icon='Zinpro', layout='wide')
st.sidebar.image("Zinpro.png", caption='Zinpro Availa')

# Define CSS styles
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
        margin-top: 150px; /* Adjust this value to add more space below the title */
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
    '<div class="fixed-title"><h1 class="header">Zinc and Chrome Study</h1><h2 class="subheader">Effects of Zinc Chrome Inclusion in Broilers Diets</h2></div>',
    unsafe_allow_html=True
)

# Main content with scrollbar
st.markdown('<div class="content">', unsafe_allow_html=True)

def main():
    with st.sidebar:
        selected = option_menu(
            menu_title='Main Menu',
            options=['Phase', 'Cumulative'],
            icons=['egg-fried', 'chicken'],
            menu_icon='cast',
            default_index=0
        )
    
    if selected == 'Phase':
        age_europa_pooled.age()
    elif selected == 'Cumulative':
         age_europa_pooled_cumulative.zinc_chrome_cumulative()

if __name__ == "__main__":
    main()



