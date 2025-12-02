import pandas as pd
import os
import codecs
import datetime
import statistics

"""
Author: Lace Ronald

This file includes basic functions for generating data objects from csv.
    
"""

def data_report(dirname, filename):
    # Used to verify data is well-formed.
    # Fix encoding error and convert to UTF-8 before reading file.
    source_encoding = 'latin1'
    source_file = os.path.join(dirname, filename)
    target_file = os.path.join(dirname, filename) + '_utf8.txt'
    with codecs.open(source_file, 'r', source_encoding) as infile:
        with codecs.open(target_file, 'w', 'utf-8') as outfile:
            outfile.write(infile.read())
    fRead = pd.read_csv(target_file)
    return fRead

def date_in_range(target_date, target_type, start_date, end_date):
    if target_date == 99999999:
        # Misformed entry at end of file.
        return False
    if target_type == 'int':
        target_date_day = target_date % 100
        target_date_month = ((target_date % 10000) - (target_date %100)) // 100
        target_date_year = target_date//10000
    elif target_type == 'str':
        target_date_day = int(target_date.split('-')[1])
        target_date_month = int(target_date.split('-')[0])
        target_date_year = int(target_date.split('-')[2])
    target = datetime.date(target_date_year, target_date_month, target_date_day)
    start_date_day = int(start_date.split('-')[1])
    start_date_month = int(start_date.split('-')[0])
    start_date_year = int(start_date.split('-')[2])
    start = datetime.date(start_date_year, start_date_month, start_date_day)
    end_date_day = int(end_date.split('-')[1])
    end_date_month = int(end_date.split('-')[0])
    end_date_year = int(end_date.split('-')[2])
    end = datetime.date(end_date_year, end_date_month, end_date_day)
    return start < target < end

def average_rate(misconduct_rates_in_range):
    rate_list = []
    for sci in misconduct_rates_in_range:
        rates = misconduct_rates_in_range[sci].values()
        for rate in rates:
            rate_list.append(rate)
    return statistics.mean(rate_list)


def rates_of_misconduct_per_year(misconduct, population):
    rates = {}
    for inst in misconduct.keys():
        rates[inst] = misconduct[inst] / population[inst]
    print("Rates of misconduct: ", rates)
    return rates

def sci_list(data_report, inst_field):
    sci_list = []
    for inst in data_report[inst_field]:
        if inst not in sci_list:
            sci_list.append(inst)
    return sci_list