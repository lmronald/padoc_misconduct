import pandas as pd
import os
import re
import plotly.express as px
#import matplotlib.pyplot as plt
import plotly.graph_objects as go
import codecs
import statistics
import re

"""
Author: Lace Ronald

This file breaks down the population data for visualization. 

Separate from the occupancy data, but may not be useful for final data visualization.

"""

def population_per_institution(data, inst_list, year):
    # Ingests the population data from physically-present-population file.
    # Outputs the institution and the average population that year.
    data_by_year = pop_by_year(data, year)
    pop_per_institution = {}
    for inst in inst_list:
        inst_data = pop_by_institution(data_by_year, inst)
        pops_by_month = []
        for pop in inst_data['DOC Physically Present Total']:
            pops_by_month.append(pop)
        pop_per_institution[inst] = statistics.mean(pops_by_month)
    return pop_per_institution

def population_per_institution_by_month_in_range(data_report, inst_list, data_category, start_date, end_date):
    # Ingests the population data from physically-present-population file.
    # Outputs the institution and the average population that year.
    start_year = int(start_date.split('-')[2])
    start_month = int(start_date.split('-')[0])
    end_month = int(end_date.split('-')[0])
    end_year = int(end_date.split('-')[2])
    year_count = end_year - start_year
    pop_per_institution = {}
    for inst in inst_list:
        month = start_month
        inst_data = pop_by_institution(data_report, inst)
        year = start_year
        pop_per_month = {}
        while year != (end_year + 1):
            month = 1
            last_month = 12
            if year == start_year:
                month = start_month
            if year == end_year:
                last_month = end_month
            while month <= last_month:
                month_str = str(month)
                if month < 10:
                    month_str = "0" + month_str
                data_by_month = pop_by_month_and_year(inst_data, month_str, start_year)
                for monthly_pop in data_by_month[data_category]:
                    pop_per_month[month_str + "-" + str(year)] = monthly_pop
                month += 1
            pop_per_institution[inst] = pop_per_month
            year += 1
    return pop_per_institution

def pop_by_institution(data, inst):
    # Filters population data to only desired institution.
    return data.loc[data['Institution'] == inst]

def pop_by_month_and_year(data_report, month, year):
    return data_report.loc[data_report['date'] == str(year) + '-' + month + '-01']

def pop_by_year(data_report, year):
    # Applies a filter variable to each entry with the desired year.
    # Change dates to year only
    data_report['date'] = data_report['date'].apply(lambda x: str(x)[:4])
    return data_report.loc[data_report['date'] == str(year)]