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

# def write_file(obj_dict):
#   Create a function here that will consume a python dictionary and output a csv file for easy read.

def miscon_per_institution(data_report, year):
        # Goes through report and creates a dictionary of misconduct counts by institution
        # Filter for preferred year by misconduct_date
        miscon_dict = {}
        for miscon in data_report:
            print(miscon)