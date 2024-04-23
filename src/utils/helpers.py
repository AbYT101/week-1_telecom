import pandas as pd

# Function to check if a pandas column is numeric
def is_numeric(column):
    try:
        pd.to_numeric(column, errors='coerce')
        print('a')
        return True
    except ValueError:
        return False
    
