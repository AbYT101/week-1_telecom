import pandas as pd
from database.database import connect_to_database  # Import your existing function for database connection
from utils.helpers import is_numeric

def load_data_from_database():
    try:
        # Establish connection to PostgreSQL database
        conn = connect_to_database()
        print('Connected to database')
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
    df.fillna(df.mean(), inplace=True)
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
