# Import necessary libraries
import pandas as pd
import sys
import os

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer

# Get the parent directory of the current script (assuming it's located in the 'src/analysis' directory)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to the system path
sys.path.insert(0, parent_dir)


from data_preparation.preprocessing import load_data_from_database, handle_missing_values, handle_outliers

# Load data
data = load_data_from_database()

if data is not None:
    # Convert 'Start' and 'End' columns to datetime format
    data['Start'] = pd.to_datetime(data['Start'])
    data['End'] = pd.to_datetime(data['End'])

    # Calculate session duration (in seconds) for each session
    data['Session_Duration'] = (data['End'] - data['Start']).dt.total_seconds()

    # Calculate total traffic (DL+UL) for each session
    data['Total_Traffic'] = data['Total DL (Bytes)'] + data['Total UL (Bytes)']
    print(data.head())
    # Compute engagement metrics per user
    user_engagement = data.groupby('MSISDN/Number').agg({
        'Bearer Id': 'count',  # Session frequency
        'Session_Duration': 'sum',  # Total session duration
        'Total_Traffic': 'sum'  # Total traffic
    }).reset_index()

    # Rename columns for clarity
    user_engagement.columns = ['MSISDN/Number', 'Session_Frequency', 'Total_Session_Duration', 'Total_Traffic']

    # Display user engagement metrics
    print("User Engagement Metrics:")
    print(user_engagement)

    # Normalize engagement metrics
    scaler = StandardScaler()
    normalized_engagement = scaler.fit_transform(user_engagement.iloc[:, 1:])

    # Run k-means clustering with k=3
    kmeans = KMeans(n_clusters=3, random_state=42)
    user_engagement['Cluster'] = kmeans.fit_predict(normalized_engagement)

    # Identify top 10 customers per engagement metric in each cluster
    top_10_customers = {}
    for cluster in range(3):
        cluster_data = user_engagement[user_engagement['Cluster'] == cluster]
        top_10_customers[cluster] = {}
        for metric in ['Session_Frequency', 'Total_Session_Duration', 'Total_Traffic']:
            top_10_customers[cluster][metric] = cluster_data.nlargest(10, metric)[['MSISDN/Number', metric]]

    # Calculate non-normalized metrics for each cluster
    cluster_metrics = user_engagement.groupby('Cluster').agg({
        'Session_Frequency': ['min', 'max', 'mean', 'sum'],
        'Total_Session_Duration': ['min', 'max', 'mean', 'sum'],
        'Total_Traffic': ['min', 'max', 'mean', 'sum']
    })

    # Display cluster metrics
    print("Cluster Metrics (Non-Normalized):")
    print(cluster_metrics)

    # Aggregate user total traffic per application
    total_traffic_per_app = data.groupby('MSISDN/Number').agg({
        'Social Media DL (Bytes)': 'sum',
        'Social Media UL (Bytes)': 'sum',
        # 'YouTube DL (Bytes)': 'sum',
        # 'YouTube UL (Bytes)': 'sum',
        'Netflix DL (Bytes)': 'sum',
        'Netflix UL (Bytes)': 'sum',
        'Google DL (Bytes)': 'sum',
        'Google UL (Bytes)': 'sum',
        'Email DL (Bytes)': 'sum',
        'Email UL (Bytes)': 'sum',
        'Gaming DL (Bytes)': 'sum',
        'Gaming UL (Bytes)': 'sum',
        # 'Other DL': 'sum',
        # 'Other UL': 'sum'
    }).reset_index()

    # Calculate total traffic per application
    total_traffic_per_app['Total_Traffic'] = total_traffic_per_app.iloc[:, 1:].sum(axis=1)

    # Derive the top 10 most engaged users per application
    top_10_per_app = {}
    for column in total_traffic_per_app.columns[1:-1]:
        top_10_per_app[column] = total_traffic_per_app.nlargest(10, column)[['MSISDN/Number', column]]

    # Display top 10 most engaged users per application
    for app, top_users in top_10_per_app.items():
        print(f"\nTop 10 most engaged users for {app}:")
        print(top_users)

    # Plot the top 3 most used applications
    # Sum up the data usage for each application
    data['Total_Data_Usage'] = data['Social Media DL (Bytes)'] + data['Social Media UL (Bytes)'] + \
                            data['Google DL (Bytes)'] + data['Google UL (Bytes)'] + \
                            data['Email DL (Bytes)'] + data['Email UL (Bytes)'] + \
                            data['Youtube DL (Bytes)'] + data['Youtube UL (Bytes)'] + \
                            data['Netflix DL (Bytes)'] + data['Netflix UL (Bytes)'] + \
                            data['Gaming DL (Bytes)'] + data['Gaming UL (Bytes)'] + \
                            data['Other DL (Bytes)'] + data['Other UL (Bytes)']

    # Get the total data usage for each application
    app_usage = data[[
                    'Google DL (Bytes)', 'Google UL (Bytes)',
                    'Email DL (Bytes)', 'Email UL (Bytes)',
                    'Youtube DL (Bytes)', 'Youtube UL (Bytes)',
                    'Netflix DL (Bytes)', 'Netflix UL (Bytes)']]

    # Sum up the data usage for each application across UL and DL
    app_usage_sum = app_usage.sum()

    # Get the top 3 applications based on total data usage
    top_3_apps = app_usage_sum.nlargest(3)
    

    # Plot the top 3 applications
    top_3_apps.plot(kind='bar', color='skyblue')
    plt.title('Top 3 Most Used Applications')
    plt.xlabel('Application')
    plt.ylabel('Total Data Usage (Bytes)')
    plt.xticks(rotation=45)
    plt.show()

    # Determine the optimized value of k using the elbow method
    X = user_engagement[['Session_Frequency', 'Total_Session_Duration', 'Total_Traffic']]
    elbow_visualizer = KElbowVisualizer(KMeans(), k=(1,11), metric='distortion', timings=False)
    elbow_visualizer.fit(X)
    elbow_visualizer.show()



