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
from misconduct import *

def control_counts_per_institution_by_month_in_range(data_report, sci_list, start_date, end_date):
    # Creates a dictionary of the min, max, and mean control numbers per institution per month in date range.
    miscons_in_range = miscon_per_institution_in_date_range(data_report, start_date, end_date)
    start_year = start_date.year
    start_month = start_date.month
    end_year = end_date.year
    end_month = end_date.month
    data_for_range = miscons_in_range
    control_per_institution = {}
    for inst in sci_list:
        control_per_month = {}
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
                control_per_month[month_str + '-' + str(year)] = control_repeats(data_by_month, inst)
                month += 1
            year += 1
        control_per_institution[inst] = control_per_month
    return control_per_institution


def control_repeats(data_report, sci):
    # Given a data report in the range, produce the mean, max, and min count for a given control number.
    # The min will most likely be 1 in all cases since we're not comparing to the list of controls outside of misconducts.
    scis_data = data_report.loc[data_report['institution'] == sci]
    mean_cont = scis_data[['institution', 'control_number']].control_number.value_counts().mean()
    max_cont = scis_data[['institution', 'control_number']].control_number.value_counts().max()
    min_cont = scis_data[['institution', 'control_number']].control_number.value_counts().min()
    return {'mean':mean_cont, 'max':max_cont, 'min':min_cont}


def check_control(data_report, sci):
    # The code below doesn't quite work. Pivoted to checking min/mean/max above.
    # Based on control number of misconduct. Look for misconducts within the same hour that have the same number and collapse them.
    control_num_dict = {}
    scis_data = data_report.loc[data_report['institution'] == sci]
    total_uncontrolled = scis_data.shape[0]
    total_controlled = total_uncontrolled
    # check for duplicate entries and subtract from total each time the control appears on the same date.
    for index, miscon_entry in scis_data.iterrows():
        control_num = miscon_entry['control_number']
        # First find all of the misconducts that match the control number
        filter_control = data_report.loc[data_report['control_number'] == control_num]
        set_on_date = filter_control.loc[filter_control['misconduct_date'] == miscon_entry['misconduct_date']]
        count_for_date = set_on_date.shape[0]
        if count_for_date > 1:
            # subtract the excess amount above 1
            total_controlled = total_controlled - (count_for_date-1)
        # print("set on same date with same control: ", set_on_date.shape)
        # key_val = str(control_num) + str(miscon_entry['misconduct_date'])
        # control_num_dict[key_val] = set_on_date.shape[0]
        #break up list by time range by the hour. If the time is more than an hour ahead or behind count it separately.
        # time_sets = {}
        # for index, miscon in set_on_date.iterrows():
        #     time = (miscon['misconduct_time'] // 100) * 100
        #     if time in time_sets:
        #         time_sets[time].append((sci, miscon_entry['misconduct_date'], control_num))
        #     else:
        #          time_sets[time] = [(sci, miscon_entry['misconduct_date'], control_num)]
        #     # Should we filter this by a time range? How do we keep track of the same control and date if the misconducts are far apart in the day?
        #     # Check that entry 'misconduct_time' is within -100 to 100 of the time on the main entry
        #     for time in time_sets.keys():
        #         key_val = str(control_num)+str(miscon_entry['misconduct_date'])+str(time)
        #         control_num_dict[key_val] = time_sets[time]
    return total_controlled, total_uncontrolled