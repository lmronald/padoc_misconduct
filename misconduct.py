import pandas as pd
import os
import re
import plotly.express as px
#import matplotlib.pyplot as plt
import plotly.graph_objects as go
import codecs


"""
Author: Lace Ronald
    
"""
def miscon_by_month_and_year(data_report, month, year):
        # Use integer math to compare year and month without regarding the day.
        year_int = int(year + month)
        return data_report.loc[data_report['misconduct_date'] // 100 == year_int]

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
                        miscon_per_institution[mis_inst] = 1
                else:
                        miscon_per_institution[mis_inst] += 1
        return miscon_per_institution

def miscon_per_institution_by_month_and_year(data_report, sci_list, year):
    miscon_per_institution = {}
    for inst in sci_list:
        miscon_per_month = {}
        data_by_inst = data_report.loc[data_report['institution'] == inst]
        month = 1
        if inst not in miscon_per_institution :
            while month < 13:
                month_str = str(month)
                if month < 10:
                    month_str = "0" + month_str
                data_by_month = miscon_by_month_and_year(data_by_inst, month_str, year)
                miscon_per_month[month_str] = data_by_month.size
                month += 1
            miscon_per_institution[inst] = miscon_per_month
    return miscon_per_institution