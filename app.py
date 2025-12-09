# Import packages
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from matplotlib.pyplot import figure

from visualization import *
from data_report import *
from data_report import *
from misconduct import *
from population import *
from output_csv import *
from visualization import *
from capacity import *
import os

YEAR = '2023'
DATE_START = '01-01-2023'
DATE_END = '12-31-2024'
MISCON = 'dbo_Miscon.txt'
POP = 'physically-present-population-23-24.csv'
CAP = 'occupancy-23-24.csv'
OCC = 'occupancy-23-24.csv'

def scis():
    return sci_list(data_report('./data_files', POP), 'Institution')

def monthly_pop_in_range():
    report = data_report('./data_files', POP)
    return population_per_institution_by_month_in_range(report, scis(), 'DOC Physically Present Total', DATE_START, DATE_END)

def monthly_miscon_rates():
    return miscon_rates_by_month_and_year(monthly_miscon_in_range(), monthly_pop_in_range(), DATE_START, DATE_END)

def monthly_miscon_in_range():
    report = data_report('./data_files', MISCON)
    return miscon_per_institution_by_month_in_range(report, scis(), DATE_START, DATE_END)

def monthly_miscon_in_range_avg_rate():
    return average_rate(monthly_miscon_rates())

def histogram(sci):
    return sci_histogram(monthly_miscon_rates()[sci], sci, monthly_miscon_in_range_avg_rate(), DATE_START, DATE_END)


df = data_report('./output', 'miscon_with_pop.csv')

app = Dash(__name__)

sci_graph_list= scis()

# histogram_dict = {}
# for sci in sci_graph_list:
#     histogram_dict[sci] = histogram(sci)

app.layout = html.Div([
    html.H1('Misconduct Rates'),
    dcc.Dropdown(id='sci-select',
                 options=sci_graph_list,
                 value=sci_graph_list[0],
                 clearable=False),
    dcc.Graph(id='histogram', figure=histogram(sci_graph_list[0]))
])

@app.callback(
    Output("histogram", "figure"),
    Input("sci-select", "value")
)
def update_histogram(input_value):
    return histogram(input_value)


if __name__ == '__main__':
    app.run(debug=True)