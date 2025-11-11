import pandas as pd
import os

"""
Author: Lace Ronald

File that takes dictionary objects on population, capacity, and misconduct then produces a reusable CSV file.

Data format:
Rows - SCI
Columns: Date (year+month), misconduct count, misconduct rate, 
        population, capacity, percent capacity, disciplinary custody count,
        administrative custody count
"""

def output_csv(misconducts, misconduct_rates, capacity, population):
    columns = ['date', 'SCI', 'misconduct count', 'misconduct rate', 'percent capacity', 'population']
    df = pd.DataFrame(misconducts)
    print("df of miscons: ", df)
    df = pd.DataFrame()
    return df.to_csv
