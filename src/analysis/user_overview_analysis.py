import pandas as pd
import sys
import os
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Get the parent directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to the system path
sys.path.insert(0, parent_dir)

from data_preparation.preprocessing import load_data_from_database, preprocess_data


# Load data
data = load_data_from_database()


if data is not None:   
    # Top 10 handsets used by customers
    top_10_handsets = data['Handset Type'].value_counts().head(10)

    # Top 3 handset manufacturers
    top_3_manufacturers = data['Handset Manufacturer'].value_counts().head(3).index.tolist()

    # Top 5 handsets per top 3 handset manufacturers
    top_5_handsets_per_manufacturer = {}
    for manufacturer in top_3_manufacturers:
        top_5_handsets = data[data['Handset Manufacturer'] == manufacturer]['Handset Type'].value_counts().head(5)
        top_5_handsets_per_manufacturer[manufacturer] = top_5_handsets

    # Interpretation and recommendations based on the analysis results
    print("Top 10 Handsets Used by Customers:")
    print(top_10_handsets)

    print("\nTop 3 Handset Manufacturers:")
    print(top_3_manufacturers)

    print("\nTop 5 Handsets per Top 3 Handset Manufacturers:")
    for manufacturer, top_5_handsets in top_5_handsets_per_manufacturer.items():
        print(f"\nManufacturer: {manufacturer}")
        print(top_5_handsets)
    
    
    # Preprocess data for missing values and outliers
    data = preprocess_data(data)
    
    # Group data by user (MSISDN/Number)
    user_data = data.groupby('MSISDN/Number')

    # Initialize dictionaries to store aggregated information
    aggregated_data = {
        'MSISDN/Number': [],
        'NumSessions': [],
        'SessionDuration': [],
        'TotalDL': [],
        'TotalUL': [],
        'TotalDataVolume': [],
        'SocialMediaDataVolume': [],
        'GoogleDataVolume': [],
        'EmailDataVolume': [],
        'YouTubeDataVolume': [],
        'NetflixDataVolume': [],
        'GamingDataVolume': [],
        'OtherDataVolume': []
    }

    # Iterate over grouped data and calculate aggregated metrics
    for msisdn, group in user_data:
        aggregated_data['MSISDN/Number'].append(msisdn)
        aggregated_data['NumSessions'].append(len(group))
        aggregated_data['SessionDuration'].append(group['Dur. (ms)'].sum())
        aggregated_data['TotalDL'].append(group['Total DL (Bytes)'].sum())
        aggregated_data['TotalUL'].append(group['Total UL (Bytes)'].sum())
        aggregated_data['TotalDataVolume'].append(group['Total DL (Bytes)'].sum() + group['Total UL (Bytes)'].sum())
        aggregated_data['SocialMediaDataVolume'].append(group['Social Media DL (Bytes)'].sum() + group['Social Media UL (Bytes)'].sum())
        aggregated_data['GoogleDataVolume'].append(group['Google DL (Bytes)'].sum() + group['Google UL (Bytes)'].sum())
        aggregated_data['EmailDataVolume'].append(group['Email DL (Bytes)'].sum() + group['Email UL (Bytes)'].sum())
        aggregated_data['YouTubeDataVolume'].append(group['Youtube DL (Bytes)'].sum() + group['Youtube UL (Bytes)'].sum())
        aggregated_data['NetflixDataVolume'].append(group['Netflix DL (Bytes)'].sum() + group['Netflix UL (Bytes)'].sum())
        aggregated_data['GamingDataVolume'].append(group['Gaming DL (Bytes)'].sum() + group['Gaming UL (Bytes)'].sum())
        aggregated_data['OtherDataVolume'].append(group['Other DL (Bytes)'].fillna(0).sum() + group['Other UL (Bytes)'].fillna(0).sum())

    # Create DataFrame from aggregated data
    aggregated_df = pd.DataFrame(aggregated_data)


    # Exploratory data analysis   
    # Describe the dataset to get basic statistics
    basic_stats = data.describe()

    # Select relevant columns for analysis
    relevant_columns = ["Dur. (ms)", "Avg Bearer TP DL (kbps)", "Avg Bearer TP UL (kbps)",
                        "Total DL (Bytes)", "Total UL (Bytes)"]

    # Subset the DataFrame with relevant columns
    relevant_data = data[relevant_columns]

    # Analyze basic metrics
    basic_metrics = {
    "Mean": relevant_data.mean(),
    "Median": relevant_data.median(),
    "Standard Deviation": relevant_data.std(),
    "Minimum": relevant_data.min(),
    "Maximum": relevant_data.max()
    }

    # Convert the basic metrics dictionary to a DataFrame for better visualization
    basic_metrics_df = pd.DataFrame(basic_metrics)

    # Print the basic metrics DataFrame
    print("Basic Metrics Analysis:")
    print(basic_metrics_df)

    # Compute dispersion parameters
    dispersion_parameters = {
        "Variance": relevant_data.var(),
        "Interquartile Range (IQR)": relevant_data.quantile(0.75) - relevant_data.quantile(0.25)
    }

    # Convert the dispersion parameters dictionary to a DataFrame for better visualization
    dispersion_parameters_df = pd.DataFrame(dispersion_parameters)

    # Print the dispersion parameters DataFrame
    print("Dispersion Parameters Analysis:")
    print(dispersion_parameters_df)


    # Select relevant columns for bivariate analysis
    relevant_columns = ["Social Media DL (Bytes)", "Social Media UL (Bytes)", 
                        "Youtube DL (Bytes)", "Youtube UL (Bytes)",
                        "Netflix DL (Bytes)", "Netflix UL (Bytes)",
                        "Google DL (Bytes)", "Google UL (Bytes)",
                        "Email DL (Bytes)", "Email UL (Bytes)",
                        "Gaming DL (Bytes)", "Gaming UL (Bytes)",
                        "Other DL (Bytes)", "Other UL (Bytes)",
                        "Total DL (Bytes)", "Total UL (Bytes)"]

    # Compute the correlation matrix for bivariate analysis
    correlation_matrix = data[relevant_columns].corr()

    # Print the correlation matrix
    print("Correlation Matrix for Bivariate Analysis:")
    print(correlation_matrix)

    # Segment users into decile classes based on total duration for all sessions
    data['Total Duration (s)'] = data['Dur. (ms)'] * data['Nb of sec with 125000B < Vol DL']
    data['Decile Class'] = pd.qcut(data['Total Duration (s)'], 10, labels=False)

    # Compute total data (DL+UL) per decile class
    total_data_per_decile = data.groupby('Decile Class')[['Total DL (Bytes)', 'Total UL (Bytes)']].sum()

    # Print the total data per decile class
    print("Total Data (DL+UL) per Decile Class:")
    print(total_data_per_decile)

    # Compute a correlation matrix for the specified variables
    correlation_matrix = data[relevant_columns].corr()

    # Print the correlation matrix
    print("Correlation Matrix:")
    print(correlation_matrix)

    # Perform principal component analysis (PCA)
    # Standardize the data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data[relevant_columns])

    # Perform PCA
    pca = PCA()
    pca.fit(scaled_data)

    # Get the principal components
    principal_components = pca.components_

    # Print the explained variance ratio
    print("\nExplained Variance Ratio:")
    print(pca.explained_variance_ratio_)

    # Interpretation of PCA results
    print("\nPrincipal Component Analysis (PCA) Interpretation:")
    print("- PCA helps to reduce the dimensionality of the data by transforming the original variables into a new set of orthogonal variables called principal components.")
    print("- Each principal component captures a certain amount of variance in the original data. The explained variance ratio shows the proportion of variance explained by each principal component.")
    print("- In this analysis, the first principal component explains the highest amount of variance, followed by the second, third, and so on.")
    print("- By retaining principal components that explain a significant amount of variance, we can reduce the dimensionality of the data while retaining most of the information.")