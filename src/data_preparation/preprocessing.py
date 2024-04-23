import pandas as pd

from database.database import connect_to_database  # Import your existing function for database connection


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
    processedData = handle_missing_values(data)
    processedData = handle_outliers(processedData)
    return preprocess_data

def handle_missing_values(df):
    # Replace missing values with the mean of the corresponding column
    df.fillna(df.mean(), inplace=True)
    return df

def handle_outliers(df):
    # Identify and treat outliers by replacing them with the mean of the corresponding column
    # We'll replace values outside 3 standard deviations with the mean
    for col in df.columns:
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

        # Optional: Save preprocessed data to file
        preprocessed_data.to_csv("processed_data.csv", index=False)
