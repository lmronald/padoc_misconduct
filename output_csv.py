import pandas as pd
import os

"""
Author: Lace Ronald

File that takes dictionary objects on population, capacity, and misconduct then produces a reusable CSV file.
"""

def output_csv(sci_list, misconducts, misconduct_rates, capacity, population, ac_status, dc_status, start_date, end_date, out_path):
    columns = ['Date', 'SCI', 'Misconduct Count', 'Misconduct Rate', 'Percent capacity', 'Population', 'Restricted Housing AC', 'Restricted Housing DC']
    rows = {}
    start_year = start_date.year
    start_month = start_date.month
    end_year = end_date.year
    end_month = end_date.month
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
                rows[date + ' ' + sci] = [date, sci, str(misconducts[sci][date]),
                                                  str(misconduct_rates[sci][date]),
                                                  str(capacity[sci][date]), str(population[sci][date]),
                                                    str(ac_status[sci][date]), str(dc_status[sci][date])]
            month += 1
        year += 1
    df = pd.DataFrame.from_dict(rows, orient='index', columns=columns)
    os.makedirs(out_path, exist_ok=True)
    return df.to_csv(out_path + "/miscon_with_pop.csv")

