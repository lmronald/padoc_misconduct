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

def average_rate(misconduct_rates_in_range):
    rate_list = []
    for sci in misconduct_rates_in_range:
        rates = misconduct_rates_in_range[sci].values()
        for rate in rates:
            rate_list.append(rate)
    print("mean: ", statistics.mean(rate_list))
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