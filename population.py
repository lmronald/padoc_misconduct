import pandas as pd
import os
import re
import plotly.express as px
#import matplotlib.pyplot as plt
import plotly.graph_objects as go
import codecs
import statistics

"""
Author: Lace Ronald

Re-use of this code is permitted under the MIT license. Property of Bucknell University.

This file includes basic functions for generating data objects from csv.

Future work here will include visualization functions for data objects.

"""

def institution_list(data):
    inst_list = []
    print(data)
    for pop_inst in data['Institution']:
        if pop_inst not in inst_list:
            inst_list.append(pop_inst)
    return inst_list

def population_per_institution(data, year):
    # Ingests the population data from physically-present-population-23-24.
    # Outputs the institution and the average population that year.
    inst_list = institution_list(data)
    filtered_data = pop_by_year(data, year)
    pop_per_institution = {}
    for inst in inst_list:
        inst_data = pop_by_institution(filtered_data, inst)
        print("pop by institution: ", inst_data)
        pops_by_month = []
        for pop in inst_data['DOC Physically Present Total']:
            pops_by_month.append(pop)
            print(pop)
        pop_per_institution[inst] = statistics.mean(pops_by_month)
    return pop_per_institution

def pop_by_institution(data, institution):
    # Filters population data to only desired institution.
    data[institution] = data['Institution'].apply(lambda  x: 1 if x == institution else 0)
    print("filter by institution: ", data[institution])
    return data[(data[institution])]

def pop_by_month_and_year(data, month, year):
    data[year] = data['date'].apply(lambda x: 1 if str(x)[:6] == (year + month) else 0)
    return data[(data[year] == 1)]
def pop_by_year(data_report, year):
    # Applies a filter variable to each entry with the desired year.
    data_report[year] = data_report['date'].apply(lambda x: 1 if str(x)[:4] == year else 0)
    return data_report[(data_report[year] == 1)]