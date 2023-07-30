import pyodbc
import pandas as pd
import os

def get_data(query):
    pass
    
def get_table_data(model_code, table_name):
    df = pd.DataFrame({
        'Column_Nbr': [1, 2, 3, 4, 5],
        'Column_Code': ['pk1', 'pk2', 'atr1', 'atr2', 'atr3'],
        'Column_Primary_Key_Flag': ['Y', 'Y', 'N', 'N', 'N'],
        'Source_Model': ['src_database', 'src_database', 'src_database', 'src_database', 'src_database'],
        'Source_Table': ['test_src_table', 'test_src_table', 'test_src_table', 'test_src_table', 'test_src_table'],
        'Source_Column': ['src_column1', 'src_column2', 'src_column3', 'src_column4', 'src_column5']
    
    })
    return df