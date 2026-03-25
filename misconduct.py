import pandas as pd
import os
import re
import plotly.express as px
#import matplotlib.pyplot as plt
import plotly.graph_objects as go
import codecs
import statistics
from data_report import *
import datetime as dt


"""
Author: Lace Ronald
    
"""

def miscon_by_month_and_year(data_report, month, year):
    miscon_by_year = data_report[data_report['misconduct_date'].dt.year == year]
    miscon_by_month = miscon_by_year[miscon_by_year['misconduct_date'].dt.month == month]
    return miscon_by_month

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
                print('institution: ', mis_inst)
                if mis_inst not in miscon_per_institution:
                        miscon_per_institution[mis_inst] = 1
                else:
                        miscon_per_institution[mis_inst] += 1
        return miscon_per_institution

def miscon_per_institution_by_month_in_range(data_report, sci_list, start_date, end_date):
    miscons_in_range = miscon_per_institution_in_date_range(data_report, start_date, end_date)
    start_year = start_date.year
    start_month = start_date.month
    end_year = end_date.year
    end_month = end_date.month
    data_for_range = miscons_in_range
    miscon_per_institution = {}
    for inst in sci_list:
        miscon_per_month = {}
        data_by_inst = data_for_range.loc[data_for_range['institution'] == inst]
        year = start_year
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
                data_by_month = miscon_by_month_and_year(data_by_inst, month, year)
                miscon_per_month[month_str + '-' + str(year)] = data_by_month.shape[0]
                month += 1
            year += 1
        miscon_per_institution[inst] = miscon_per_month
    return miscon_per_institution


def miscon_per_institution_in_date_range(data_report, start_date, end_date):
    data_report = data_report.drop(data_report[data_report.misconduct_date == 99999999].index)
    data_report['misconduct_date'] = pd.to_datetime(data_report['misconduct_date'].astype(str), format="%Y%m%d")
    miscons = data_report[data_report['misconduct_date'] > start_date]
    miscons_in_range = miscons[miscons['misconduct_date'] < end_date]
    return miscons_in_range

def miscon_rates_by_month_and_year(miscons, populations, start_date, end_date):
    # Take population and misconduct dictionaries by month and year and produce the misconduct rates for those months.
    start_year = start_date.year
    start_month = start_date.month
    end_year = end_date.year
    end_month = end_date.month
    rates = {}
    for sci in populations:
        monthly_rate = {}
        year = start_year
        while year != (end_year + 1):
            month = 1
            last_month = 12
            if year == start_year:
                month = start_month
            if year == end_year:
                last_month = end_month
            sci_miscons = miscons[sci]
            sci_pops = populations[sci]
            while month <= last_month:
                month_str = str(month)
                if month < 10:
                    month_str = "0" + str(month)
                monthly_rate[month_str + '-' + str(year)] = (sci_miscons[month_str + '-' + str(year)]/sci_pops[month_str + '-' + str(year)])
                month += 1
            year += 1
        rates[sci] = monthly_rate
    return rates

def form_141_counts(data_report, sci_list, year):
    # Disciplinary custody = 801
    # Administrative custody = 802
    # Goes through the 141 counts by month.
    # TODO: fix the bug in this that's not counting all of the misconducts.
    form_141_per_institution = {}
    for inst in sci_list:
        form_141_per_month = {}
        data_by_inst = data_report.loc[data_report['institution'] == inst]
        month = 1
        while month < 13:
                month_str = str(month)
                if month < 10:
                    month_str = "0" + month_str
                data_by_month = miscon_by_month_and_year(data_by_inst, month_str, year)
                admin_count = 0
                discp_count = 0
                print("form vals: ", data_by_month['form_141'])
                # Why are some form values not showing despite size of month data being in the 1000+?
                for form_val in data_by_month['form_141']:
                    if int(form_val) == 801:
                        discp_count += 1
                    elif int(form_val) == 802:
                        admin_count += 1
                form_141_per_month[month_str] = {"Disciplinary Custody": discp_count, "Administrative Custody": admin_count}
                month += 1
        form_141_per_institution[inst] = form_141_per_month
    print("form 141: ", form_141_per_institution)
    return form_141_per_institution

def sci_check(data_report, sci_name, year):
    # get SCI data from a given institution and year.
    sci_data = data_report.loc[data_report['institution'] == sci_name]
    return sci_data.loc[sci_data['misconduct_date']//10000 == year]