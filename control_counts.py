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


def control_repeats(data_report, sci):
    # got through each SCI, each month, count how frequently each control number appears. Find average?
    # assumes data_report is in range
    scis_data = data_report.loc[data_report['institution'] == sci]
    print("control counts: ", scis_data.control_number.value_counts())
    print (scis_data[['institution', 'control_number']].control_number.value_counts().mean())
    print(scis_data[['institution', 'control_number']].control_number.value_counts().max())
    print(scis_data[['institution', 'control_number']].control_number.value_counts().min())
    return "printed control repeats"


def check_control(data_report, sci):
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