import pandas as pd
import sys
import os

# Get the parent directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to the system path
sys.path.insert(0, parent_dir)

import streamlit as st
from dashboard.visualization import visualize_top_handsets, visualize_top_manufacturers, visualize_top_5_handsets_per_manufacturer
from analysis.user_overview_analysis import get_top_10_handsets, get_top_3_manufacturers, get_top_5_handsets_per_manufacturer

def main():
    st.title("User Overview Analysis")
    
    # Load and preprocess data
    # ...
    
    # Display data overview
    st.header("Data Overview")
    st.write("Insert summary statistics or general overview here.")
    
    # Data visualization
    st.header("Data Visualization")
    st.subheader("Histogram")
    visualize_top_handsets(get_top_10_handsets())  
    
    st.subheader("Box Plot")
    visualize_top_manufacturers(get_top_3_manufacturers())  

    st.subheader("")
    visualize_top_5_handsets_per_manufacturer(get_top_5_handsets_per_manufacturer())

if __name__ == "__main__":
    main()
