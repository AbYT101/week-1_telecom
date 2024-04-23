import sys
sys.path.append("../../")
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer

from src.data_preparation.preprocessing import load_data_from_database, handle_missing_values, handle_outliers

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

    # Compute engagement metrics per user
    user_engagement = data.groupby('MSISDN/Number').agg({
        'bearer id': 'count',  # Session frequency
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
        'YouTube DL (Bytes)': 'sum',
        'YouTube UL (Bytes)': 'sum',
        'Netflix DL (Bytes)': 'sum',
        'Netflix UL (Bytes)': 'sum',
        'Google DL (Bytes)': 'sum',
        'Google UL (Bytes)': 'sum',
        'Email DL (Bytes)': 'sum',
        'Email UL (Bytes)': 'sum',
        'Gaming DL (Bytes)': 'sum',
        'Gaming UL (Bytes)': 'sum',
        'Other DL': 'sum',
        'Other UL': 'sum'
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
    top_3_apps = ['Social Media', 'Google', 'YouTube']
    total_traffic_top_3 = data[top_3_apps].sum()

    plt.figure(figsize=(10, 6))
    total_traffic_top_3.sort_values().plot(kind='barh', color='skyblue')
    plt.title('Top 3 Most Used Applications')
    plt.xlabel('Total Traffic (Bytes)')
    plt.ylabel('Application')
    plt.show()

    # Determine the optimized value of k using the elbow method
    X = customer_engagement[['Session_Frequency', 'Total_Session_Duration', 'Total_Traffic']]
    elbow_visualizer = KElbowVisualizer(KMeans(), k=(1,11), metric='distortion', timings=False)
    elbow_visualizer.fit(X)
    elbow_visualizer.show()



