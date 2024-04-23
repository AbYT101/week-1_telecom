import pandas as pd
from database.database import connect_to_database  # Import your existing function for database connection
from utils.helpers import is_numeric

def load_data_from_database():
    try:
        # Establish connection to PostgreSQL database
        conn = connect_to_database()

        # Query data from database
        query = "SELECT * FROM public.xdr_data;"
        data = pd.read_sql(query, conn)

        # Close database connection
        conn.dispose()

        return data

    except Exception as e:
        print("Error loading data from PostgreSQL database:", e)
        return None


def preprocess_data(data):
    # Perform all data preprocessing steps here
    processed_data = handle_missing_values(data)
    processed_data = handle_outliers(processed_data)

    return processed_data

def handle_missing_values(df: pd.DataFrame):
    # Replace missing values with the mean of the corresponding column
    df['Dur. (ms)'] = df['Dur. (ms)'].fillna(df['Dur. (ms)'].mean())
    df['Total DL (Bytes)'] = df['Total DL (Bytes)'].fillna(df['Total DL (Bytes)'].mean())
    df['Total UL (Bytes)'] = df['Total UL (Bytes)'].fillna(df['Total UL (Bytes)'].mean())
    df['Social Media DL (Bytes)'] = df['Social Media DL (Bytes)'].fillna(df['Social Media DL (Bytes)'].mean())
    df['Social Media UL (Bytes)'] = df['Social Media UL (Bytes)'].fillna(df['Social Media UL (Bytes)'].mean())
    df['Google DL (Bytes)'] = df['Google DL (Bytes)'].fillna(df['Google DL (Bytes)'].mean())
    df['Google UL (Bytes)'] = df['Google UL (Bytes)'].fillna(df['Google UL (Bytes)'].mean())
    df['Email DL (Bytes)'] = df['Email DL (Bytes)'].fillna(df['Email DL (Bytes)'].mean())
    df['Email UL (Bytes)'] = df['Email UL (Bytes)'].fillna(df['Email UL (Bytes)'].mean())
    df['Youtube DL (Bytes)'] = df['Youtube DL (Bytes)'].fillna(df['Youtube DL (Bytes)'].mean())
    df['Youtube UL (Bytes)'] = df['Youtube UL (Bytes)'].fillna(df['Youtube UL (Bytes)'].mean())
    df['Netflix DL (Bytes)'] = df['Netflix DL (Bytes)'].fillna(df['Netflix DL (Bytes)'].mean())
    df['Netflix UL (Bytes)'] = df['Netflix UL (Bytes)'].fillna(df['Netflix UL (Bytes)'].mean())
    df['Gaming DL (Bytes)'] = df['Gaming DL (Bytes)'].fillna(df['Gaming DL (Bytes)'].mean())
    df['Gaming UL (Bytes)'] = df['Gaming UL (Bytes)'].fillna(df['Gaming UL (Bytes)'].mean())
    df['Other DL (Bytes)'] = df['Other DL (Bytes)'].fillna(df['Other DL (Bytes)'].mean())
    df['Other UL (Bytes)'] = df['Other UL (Bytes)'].fillna(df['Other UL (Bytes)'].mean())
    return df

def handle_outliers(df):
    # Identify and treat outliers by replacing them with the mean of the corresponding column
    # We'll replace values outside 3 standard deviations with the mean
    numeric_columns = [
        "Social Media DL (Bytes)", "Social Media UL (Bytes)",
        "Google DL (Bytes)", "Google UL (Bytes)",
        "Email DL (Bytes)", "Email UL (Bytes)",
        "Youtube DL (Bytes)", "Youtube UL (Bytes)",
        "Netflix DL (Bytes)", "Netflix UL (Bytes)",
        "Gaming DL (Bytes)", "Gaming UL (Bytes)",
        "Other DL (Bytes)", "Other UL (Bytes)",
        "Total UL (Bytes)", "Total DL (Bytes)"
    ]
    for col in numeric_columns:
        mean_val = df[col].mean()
        std_val = df[col].std()
        lower_bound = mean_val - 3 * std_val
        upper_bound = mean_val + 3 * std_val
        df[col] = df[col].apply(lambda x: mean_val if x < lower_bound or x > upper_bound else x)
    
    return df


if __name__ == "__main__":
    # Load data
    data = load_data_from_database()

    if data is not None:
        # Preprocess data
        preprocessed_data = preprocess_data(data)
