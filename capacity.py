import pandas as pd
import os
import re
from population import *

"""
Author: Lace Ronald

"""

def capacity_per_institution_by_month_in_range(data_report, inst_list, start_date, end_date):
    # Ingests the population data from physically-present-population file.
    # Outputs the institution and the average population that year.
    start_year = start_date.year
    start_month = start_date.month
    end_year = end_date.year
    end_month = end_date.month

    data = update_sci_names(data_report)
    cap_per_institution = {}
    for inst in inst_list:
        cap_per_month = {}
        inst_data = cap_by_institution(data, inst)
        month = start_month
        year = start_year
        while year != (end_year + 1):
            month = 1
            last_month = 12
            if year == start_year:
                month = start_month
            if year == end_year:
                last_month = end_month
            while month <= last_month:
                if month < 10:
                    month_str = "0" + str(month)
                else:
                    month_str = str(month)
                data_by_month = cap_by_month_and_year(inst_data, month_str, year)
                for monthly_cap in data_by_month['Percent of capacity']:
                    cap_per_month[month_str + "-" + str(year)] = monthly_cap
                month += 1
                cap_per_institution[inst] = cap_per_month
            cap_per_institution[inst] = cap_per_month
            year += 1
    return cap_per_institution


def update_sci_names(data):
    # Edit SCI names to abbreviations
    data['Institution'] = data['Institution'].apply(lambda x: x[-4:-1])
    return data

def cap_by_institution(data, inst):
    # Filters population data to only desired institution.
    return data.loc[data['Institution'] == inst]

def cap_by_month_and_year(data_report, month, year):
    return data_report.loc[data_report['date'] == str(year) + '-' + month + '-01']