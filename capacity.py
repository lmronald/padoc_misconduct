import pandas as pd
import os
import re
from population import *

"""
Author: Lace Ronald

"""

def capacity_per_institution_by_month_and_year(data, year):
    # Ingests the population data from physically-present-population file.
    # Outputs the institution and the average population that year.'
    print("Data: ", data)
    data = update_sci_names(data)
    inst_list = institution_list(data)
    cap_per_institution = {}
    for inst in inst_list:
        cap_per_month = {}
        month = 1
        inst_data = cap_by_institution(data, inst)
        while month < 13:
            if month < 10:
                month_str = "0" + str(month)
            else:
                month_str = str(month)
            data_by_month = cap_by_month_and_year(inst_data, month_str, year)
            for monthly_cap in data_by_month['Percent of capacity']:
                cap_per_month[month_str] = monthly_cap
            month += 1
            cap_per_institution[inst] = cap_per_month
    return cap_per_institution

def update_sci_names(data):
    # Edit SCI names to abbreviations
    data['Institution'] = data['Institution'].apply(lambda x: x[-4:-1])
    return data

def cap_by_institution(data, inst):
    # Filters population data to only desired institution.
    return data.loc[data['Institution'] == inst]

def cap_by_month_and_year(data_report, month, year):
    return data_report.loc[data_report['date'] == year + '-' + month + '-01']