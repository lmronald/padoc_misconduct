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

This file includes basic functions for generating data objects from csv.

Future work here will include visualization functions for data objects.
    
"""

# def write_file(obj_dict):
#   Create a function here that will consume a python dictionary and output a csv file for easy read.


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

def rates_of_misconduct_per_year(misconduct, population):
    rates = {}
    for inst in misconduct.keys():
        rates[inst] = misconduct[inst] / population[inst]
    print("Rates of misconduct: ", rates)
    return rates