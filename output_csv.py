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

def output_csv(sci_list, misconducts, misconduct_rates, capacity, population, start_date, end_date, out_path):
    columns = ['date', 'SCI', 'misconduct count', 'misconduct rate', 'percent capacity', 'population']
    rows = {}
    start_year = int(start_date.split('-')[2])
    start_month = int(start_date.split('-')[0])
    end_month = int(end_date.split('-')[0])
    end_year = int(end_date.split('-')[2])
    year = start_year
    while year != (end_year + 1):
        month = 1
        last_month = 12
        if year == start_year:
            month = start_month
        if year == end_year:
            last_month = end_month
        while month <= last_month:
            month_str = "0" + str(month) if month < 10 else str(month)
            date = month_str + "-" + str(year)
            for sci in sci_list:
                print("SCI: ", sci, " ", date)
                rows[date + ' ' + sci] = [date, sci, str(misconducts[sci][date]),
                                                  str(misconduct_rates[sci][date]),
                                                  str(capacity[sci][date]), str(population[sci][date])]
            month += 1
        year += 1
    df = pd.DataFrame.from_dict(rows, orient='index', columns=columns)
    print("data frame for CSV: ", df)
    os.makedirs(out_path, exist_ok=True)
    return df.to_csv(out_path + "/miscon_with_pop.csv")

