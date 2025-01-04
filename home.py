import streamlit as st
import emoji
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from streamlit_extras.metric_cards import style_metric_cards


#Custom CSS to change the background color
page_bg_style = """ <style> [data-testid="stAppViewContainer"] {background-color: #96c3eb; } </style> """

# Inject the CSS into the app
st.markdown(page_bg_style, unsafe_allow_html=True)



# Title
st.markdown('<h1 style="color: #008000; font-size: 3.0em; font-weight: bold;">IBNR Calculation Model</h1>',
    unsafe_allow_html=True)

#Display image
#st.image("cool emoji.jpg"),use_column_width=False)

st.write(emoji.emojize("Welcome to my mini project for calculating IBNR 😍😍"))

# Upload claims triangle
uploaded_file = st.file_uploader("UPLOAD CLAIMS TRIANGLE CSV", type="csv")
if uploaded_file:
    # Read the data
    claims_triangle = pd.read_csv(uploaded_file, index_col=0)
    #st.subheader("Uploaded Claims Triangle")
    st.markdown('<h1 style="color: #008000; font-size: 2.0em; font-weight: bold;">Uploaded Claims Triangle</h1>',
    unsafe_allow_html=True)
    st.dataframe(claims_triangle)

    
    # Calculate development factors
    dev_factors = []
    for col in range(claims_triangle.shape[1] - 1):
        col_sum = claims_triangle.iloc[:, col + 1].sum() / claims_triangle.iloc[:, col].sum()
        dev_factors.append(col_sum)
    
    # Append the last factor as 1 (tail factor)
    dev_factors.append(1.0)
    
    #st.subheader("Development Factors")
    st.markdown('<h1 style="color: #008000; font-size: 2.0em; font-weight: bold;">Development Factors</h1>',
    unsafe_allow_html=True)
    st.write(dev_factors)
    

    # Project future values
    proj_triangle = claims_triangle.copy()
    for col in range(claims_triangle.shape[1] - 1):
        for row in range(len(claims_triangle)):
            if pd.isna(proj_triangle.iloc[row, col + 1]):
                proj_triangle.iloc[row, col + 1] = proj_triangle.iloc[row, col] * dev_factors[col]

    #st.subheader("Projected Claims Triangle")
    st.markdown('<h1 style="color: #008000; font-size: 2.0em; font-weight: bold;">Projected Claims Triangle</h1>',
    unsafe_allow_html=True)
    st.dataframe(proj_triangle)

    # Calculate IBNR
    total_reported = claims_triangle.sum().sum()
    total_projected = proj_triangle.sum().sum()
    ibnr = total_projected - total_reported
    ibnr = round(ibnr,2)

    
    st.markdown('<h1 style="color: #008000; font-size: 2.0em; font-weight: bold;">IBNR Estimate</h1>',
    unsafe_allow_html=True)
    #st.write(f"IBNR: GHS {ibnr:,}")

    st.metric(label='IBNR ESTIMATE',value=f"IBNR: GHS {ibnr:,} 💰💰")
    style_metric_cards(
    background_color='white',
    border_size_px=2,
    border_color='green',
    border_radius_px=5,
    border_left_color='green',
    box_shadow=True, 
    )


    # Visualize
    # st.subheader("Triangle Visualization")
    # fig, ax = plt.subplots()
    # ax.matshow(proj_triangle, cmap='coolwarm', alpha=0.7)
    # for (i, j), val in np.ndenumerate(proj_triangle):
    #     ax.text(j, i, f'{val:.0f}', ha='center', va='center')
    # st.pyplot(fig)