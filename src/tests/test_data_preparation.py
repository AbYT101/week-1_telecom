import unittest
import pandas as pd
import numpy as np
import sys
import os

# Get the parent directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to the system path
sys.path.insert(0, parent_dir)

from data_preparation.preprocessing import handle_missing_values

class TestHandleMissingValues(unittest.TestCase):
    def test_handle_missing_values(self):
        # Create a sample DataFrame with missing values
        df = pd.DataFrame({'A': [1, 2, np.nan, 4], 'B': [5, np.nan, 7, 8]})
        
        # Call the function to handle missing values
        df_cleaned = handle_missing_values(df)
        
        # Check that missing values are replaced with the mean
        self.assertFalse(df_cleaned.isnull().values.any())
        
        # Check that the mean values are correct
        self.assertAlmostEqual(df_cleaned['A'].mean(), 2.333, places=3)
        self.assertAlmostEqual(df_cleaned['B'].mean(), 6.667, places=3)

if __name__ == '__main__':
    unittest.main()
