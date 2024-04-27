import sys, os

# Get the parent directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to the system path
sys.path.insert(0, parent_dir)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances

from data_preparation.preprocessing import load_data_from_database, preprocess_data


np.random.seed(42)
num_users = 1000
num_features = 5

user_data = np.random.rand(num_users, num_features)

num_clusters = 3
engagement_centroids = np.random.rand(num_clusters, num_features)
experience_centroids = np.random.rand(num_clusters, num_features)

engagement_scores = euclidean_distances(user_data, engagement_centroids).min(axis=1)

# Calculate Euclidean distance between each user and the worst experience cluster
experience_scores = euclidean_distances(user_data, experience_centroids).min(axis=1)

satisfaction_scores = (engagement_scores + experience_scores) / 2

# Generate some sample user IDs for demonstration
user_ids = ['user_' + str(i) for i in range(num_users)]

# Combine the scores with user IDs
satisfaction_df = pd.DataFrame({'MSISDN/Number': user_ids, 
                                 'Engagement Score': engagement_scores,
                                 'Experience Score': experience_scores,
                                 'Satisfaction Score': satisfaction_scores})

# Report the top 10 satisfied customers
top_10_satisfied_customers = satisfaction_df.nlargest(10, 'Satisfaction Score')

# Generate some sample feature matrix X and target variable y for demonstration
X = np.random.rand(num_users, num_features)
y = satisfaction_scores  # Using satisfaction scores as the target variable

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and fit the model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Calculate RMSE (Root Mean Squared Error)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# Run k-means clustering (k=2) on the combined engagement and experience scores
kmeans = KMeans(n_clusters=2)
cluster_labels = kmeans.fit_predict(np.column_stack((engagement_scores, experience_scores)))

# Add cluster labels to satisfaction_df
satisfaction_df['Cluster'] = cluster_labels

# Aggregate average satisfaction and experience score per cluster
cluster_agg = satisfaction_df.groupby('Cluster').agg({'Satisfaction Score': 'mean', 
                                                       'Experience Score': 'mean'})
