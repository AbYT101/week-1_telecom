import pandas as pd
import sys
import os

# Get the parent directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to the system path
sys.path.insert(0, parent_dir)

from data_preparation.preprocessing import load_data_from_database, preprocess_data

# Methods
# Aggregate user information
def aggregate_user_info(df):
    # Group by customer (MSISDN) and calculate the mean for each column
    aggregated_df = df.groupby('MSISDN/Number').agg({
        'TCP DL Retrans. Vol (Bytes)': 'mean',
        'Avg RTT DL (ms)': 'mean',
        'Handset Type': lambda x: x.mode().iloc[0],
        'Avg Bearer TP DL (kbps)': 'mean'
    }).reset_index()
    
    return aggregated_df

# Compute the top, bottom, and most frequent values for the given column
def compute_top_bottom_frequent(df, column_name):
    top_values = df[column_name].nlargest(10).values
    bottom_values = df[column_name].nsmallest(10).values
    frequent_values = df[column_name].value_counts().nlargest(10).index.tolist()
    
    return top_values, bottom_values, frequent_values


# Load data
data = load_data_from_database()

if data is not None:   
    # Preprocess data for missing values and outliers
    # data = preprocess_data(data)

    # Aggregate user information
    aggregated_user_info = aggregate_user_info(data)

    # Display the aggregated user information
    print("Aggregated user information:", aggregated_user_info.head())

    # Compute top, bottom, and most frequent values for TCP
    top_tcp, bottom_tcp, frequent_tcp = compute_top_bottom_frequent(data, 'TCP DL Retrans. Vol (Bytes)')

    # Compute top, bottom, and most frequent values for RTT
    top_rtt, bottom_rtt, frequent_rtt = compute_top_bottom_frequent(data, 'Avg RTT DL (ms)')

    # Compute top, bottom, and most frequent values for Throughput
    top_throughput, bottom_throughput, frequent_throughput = compute_top_bottom_frequent(data, 'Avg Bearer TP DL (kbps)')

    # Display the results
    print("Top TCP values:", top_tcp)
    print("Bottom TCP values:", bottom_tcp)
    print("Most frequent TCP values:", frequent_tcp)
    print("\nTop RTT values:", top_rtt)
    print("Bottom RTT values:", bottom_rtt)
    print("Most frequent RTT values:", frequent_rtt)
    print("\nTop Throughput values:", top_throughput)
    print("Bottom Throughput values:", bottom_throughput)
    print("Most frequent Throughput values:", frequent_throughput)

    # Compute the average throughput per handset type
    average_throughput_per_handset = data.groupby('Handset Type')['Avg Bearer TP DL (kbps)'].mean()

    # Compute the average TCP retransmission per handset type
    average_tcp_retransmission_per_handset = data.groupby('Handset Type')['TCP DL Retrans. Vol (Bytes)'].mean()

    # Report the distribution of the average throughput per handset type
    print("Distribution of Average Throughput per Handset Type:")
    print(average_throughput_per_handset)

    # Report the average TCP retransmission per handset type
    print("\nAverage TCP Retransmission per Handset Type:")
    print(average_tcp_retransmission_per_handset)
