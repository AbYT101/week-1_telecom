import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_top_handsets(handset_counts):
    # Plotting
    st.title("Top 10 Handsets Used")
    plt.figure(figsize=(10, 6))
    sns.barplot(x=handset_counts.values, y=handset_counts.index, palette='viridis')
    plt.xlabel('Number of Users')
    plt.ylabel('Handset Type')
    plt.title('Top 10 Handsets Used')
    plt.xticks(rotation=45)
    st.pyplot(plt)

def visualize_top_manufacturers(manufacturer_counts):
    # Plotting
    st.title("Top 3 Manufacturers")
    plt.figure(figsize=(8, 6))
    sns.barplot(x=manufacturer_counts.values, y=manufacturer_counts.index, palette='muted')
    plt.xlabel('Number of Users')
    plt.ylabel('Manufacturer')
    plt.title('Top 3 Manufacturers')
    st.pyplot(plt)


def visualize_top_5_handsets_per_manufacturer(top_5_handsets_per_manufacturer):
    st.title("Top 5 Handsets Per Manufacturer")
    
    for manufacturer, top_5_handsets in top_5_handsets_per_manufacturer.items():
        # Plotting
        plt.figure(figsize=(8, 6))
        sns.barplot(x=top_5_handsets.values, y=top_5_handsets.index, palette='muted')
        plt.xlabel('Number of Users')
        plt.ylabel('Handset Type')
        plt.title(f'Top 5 Handsets for {manufacturer}')
        plt.xticks(rotation=45)
        st.pyplot(plt)
