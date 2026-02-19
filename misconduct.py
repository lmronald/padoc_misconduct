import pandas as pd
import os
import re
import plotly.express as px
#import matplotlib.pyplot as plt
import plotly.graph_objects as go
import codecs
import statistics
from data_report import *


"""
Author: Lace Ronald
    
"""

def miscon_by_month_and_year(data_report, month, year):
        # Use integer math to compare year and month without regarding the day.
        date_int = int(year)*100 + int(month)
        return data_report.loc[data_report['misconduct_date'] // 100 == date_int]

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
    start_year = int(start_date.split('-')[2])
    start_month = int(start_date.split('-')[0])
    end_month = int(end_date.split('-')[0])
    end_year = int(end_date.split('-')[2])
    data_for_range = data_report
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
                data_by_month = miscon_by_month_and_year(data_by_inst, month_str, year)
                miscon_per_month[month_str + '-' + str(year)] = data_by_month.size
                month += 1
            year += 1
        miscon_per_institution[inst] = miscon_per_month
    return miscon_per_institution

def check_control(data_report, sci):
    # Based on control number of misconduct. Look for misconducts within the same hour that have the same number and collapse them.
    control_num_dict = {}
    scis_data = data_report.loc[data_report['institution'] == sci]
    total_uncontrolled = scis_data.size
    for index, miscon_entry in scis_data.iterrows():
        control_num = miscon_entry['control_number']
        # First find all of the misconducts that match the control number
        filter_control = data_report.loc[data_report['control_number'] == control_num]
        set_on_date = filter_control.loc[filter_control['misconduct_date'] == miscon_entry['misconduct_date']]
        #break up list by time range by the hour. If the time is more than an hour ahead or behind count it separately.
        time_sets = {}
        for index, miscon in set_on_date.iterrows():
            time = (miscon['misconduct_time'] // 100) * 100
            if time in time_sets:
                time_sets[time].append((sci, miscon_entry['misconduct_date'], control_num))
            else:
                 time_sets[time] = [(sci, miscon_entry['misconduct_date'], control_num)]
            # Should we filter this by a time range? How do we keep track of the same control and date if the misconducts are far apart in the day?
            # Check that entry 'misconduct_time' is within -100 to 100 of the time on the main entry
            for time in time_sets.keys():
                key_val = str(control_num)+str(miscon_entry['misconduct_date'])+str(time)
                control_num_dict[key_val] = time_sets[time]
    return control_num_dict, total_uncontrolled


def miscon_per_institution_in_date_range(data_report, start_date, end_date):
    data_report['in_range'] = data_report['misconduct_date'].apply(lambda x: date_in_range(x,'int', start_date, end_date))
    return data_report[(data_report['in_range'])]

def miscon_rates_by_month_and_year(miscons, populations, start_date, end_date):
    # Take population and misconduct dictionaries by month and year and produce the misconduct rates for those months.
    start_year = int(start_date.split('-')[2])
    start_month = int(start_date.split('-')[0])
    end_month = int(end_date.split('-')[0])
    end_year = int(end_date.split('-')[2])
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
            while month < 13:
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
                print("size of month data: ", data_by_month.size)
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