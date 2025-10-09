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

def institution_list(data):
    inst_list = []
    print(data)
    for pop_inst in data['Institution']:
        if pop_inst not in inst_list:
            inst_list.append(pop_inst)
    return inst_list

def population_per_institution(data, year):
    # Ingests the population data from physically-present-population file.
    # Outputs the institution and the average population that year.
    inst_list = institution_list(data)
    data_by_year = pop_by_year(data, year)
    pop_per_institution = {}
    for inst in inst_list:
        inst_data = pop_by_institution(data_by_year, inst)
        pops_by_month = []
        for pop in inst_data['DOC Physically Present Total']:
            pops_by_month.append(pop)
        if inst == 'WAM':
            #This institution is coded in the data with a * after it and I'm not sure why.
            pop_per_institution[inst] = pop_per_institution['WAM*']
        else:
            pop_per_institution[inst] = statistics.mean(pops_by_month)
    return pop_per_institution

def population_per_institution_by_month_and_year(data, year):
    # Ingests the population data from physically-present-population file.
    # Outputs the institution and the average population that year.
    inst_list = institution_list(data)
    pop_per_institution = {}
    for inst in inst_list:
        pop_per_month = {}
        month = 1
        inst_data = pop_by_institution(data, inst)
        while month < 13:
            month_str = str(month)
            if month < 10:
                month_str = "0" + month_str
            data_by_month = pop_by_month_and_year(inst_data, month_str, year)
            for monthly_pop in data_by_month['DOC Physically Present Total']:
                pop_per_month[month_str] = monthly_pop
            month += 1
        if inst == 'WAM':
            #This institution is coded in the data with a * after it and I'm not sure why.
            pop_per_institution[inst] = pop_per_institution['WAM*']
        else:
            pop_per_institution[inst] = pop_per_month
    return pop_per_institution

def pop_by_institution(data, inst):
    # Filters population data to only desired institution.
    return data.loc[data['Institution'] == inst]

def pop_by_month_and_year(data_report, month, year):
    return data_report.loc[data_report['date'] == year + '-' + month + '-01']

def pop_by_year(data_report, year):
    # Applies a filter variable to each entry with the desired year.
    # Change dates to year only
    data_report['date'] = data_report['date'].apply(lambda x: str(x)[:4])
    return data_report.loc[data_report['date'] == year]