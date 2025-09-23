import pandas as pd
import os
import re
import plotly.express as px
#import matplotlib.pyplot as plt
import plotly.graph_objects as go
import codecs


"""
Author: Lace Ronald
    
Re-use of this code is permitted under the MIT license. Property of Bucknell University.
    
"""
def miscon_by_month_and_year(data_report, month, year):
        #need to rewrite to avoid filtering like this and match up with population function.
        # TODO: fix this and then re-check compiling.
        data_report[year] = data_report['misconduct_date'].apply(lambda x: 1 if str(x)[:6] == (year + month) else 0)
        return data_report[(data_report[year] == 1)]

def miscon_by_year(data_report, year):
        # Applies a filter variable to each entry with the desired year.
        data_report[year] = data_report['misconduct_date'].apply(lambda x: 1 if str(x)[:4] == year else 0)
        return data_report[(data_report[year] == 1)]

def miscon_per_institution(data_report, year):
        # Goes through report and creates a dictionary of misconduct counts by institution
        # Filter for preferred year by misconduct_date
        filtered_data = miscon_by_year(data_report, year)
        miscon_per_institution = {}
        for mis_inst in filtered_data['institution']:
                if mis_inst not in miscon_per_institution:
                        miscon_per_institution[mis_inst] = 0
                else:
                        miscon_per_institution[mis_inst] += 1
        return miscon_per_institution

def miscon_per_institution_by_month_and_year(data_report, year):
    inst_data = miscon_by_year(data_report, year)
    miscon_per_institution = {}
    for inst in inst_data['institution']:
        miscon_per_month = {}
        month = 1
        while month < 13:
            month_str = str(month)
            if month < 10:
                month_str = "0" + month_str
            data_by_month = miscon_by_month_and_year(inst_data, month_str, year)
            for monthly_pop in data_by_month['FIX THIS']:
                miscon_per_month[month_str] = monthly_pop
            month += 1
            miscon_per_institution[inst] = miscon_per_month
    return miscon_per_institution