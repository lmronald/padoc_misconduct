import pandas as pd
import os
import re
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from matplotlib.pyplot import legend
from plotly.validator_cache import ValidatorCache
import matplotlib.pyplot as pyplot
import statistics

"""
Graph visualizations of misconduct and population data across SCis.

Author: Lace Ronald
"""

def all_sci_scatter_plot(misconducts, capacity, year):
    fig = go.Figure()
    SymbolValidator = ValidatorCache.get_validator("scatter.marker", "symbol")
    raw_symbols = SymbolValidator.values
    namestems = []
    namevariants = []
    symbols = []
    for i in range(0, len(raw_symbols), 3):
        name = raw_symbols[i + 2]
        symbols.append(raw_symbols[i])
        namestems.append(name.replace("-open", "").replace("-dot", ""))
        namevariants.append(name[len(namestems[-1]):])
    for inst in capacity:
        miscon_inst = misconducts[inst]
        pop_inst = capacity[inst]
        sorted_miscon = sorted(miscon_inst)
        sorted_pop = sorted(pop_inst)
        miscon = [miscon_inst[key] for key in sorted_miscon]
        pop = [pop_inst[key] for key in sorted_pop]
        fig.add_trace(go.Scatter(
            x=pop,
            y=miscon,
            mode="markers+text",
            marker_symbol=symbols,
            name= inst + " " + year,
            text=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
                  "Oct", "Nov", "Dec"],
            textposition="top center"
        ))
    fig.update_layout(
        title="Misconduct and Population for " + year,
        xaxis_title="Percent Capacity by Month",
        yaxis_title="Misconduct Rate by Month"
    )
    fig.show()

def sci_scatter_plot(sci_miscon, sci_population, sci, year):
    # Take dictionaries of SCI by month for population and misconduct.
    # TODO: Update misconduct to be based on rate.
    sorted_miscon = sorted(sci_miscon)
    sorted_pop = sorted(sci_population)
    miscon = [sci_miscon[key] for key in sorted_miscon]
    pop = [sci_population[key] for key in sorted_pop]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=pop,
        y=miscon,
        mode="markers+text",
        name=sci + " " + year,
        text=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
              "Oct", "Nov", "Dec"],
        textposition="top center"
    ))
    fig.update_layout(
        title="Misconduct and Population for " + year,
        xaxis_title="Population by Month",
        yaxis_title="Misconduct by Month"
    )
    fig.show()

def sci_bar_plot(sci_miscon, sci, year):
    # Take dictionaries of SCI by month for population and misconduct.
    sorted_miscon = sorted(sci_miscon)
    miscon = [sci_miscon[key] for key in sorted_miscon]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
              "Oct", "Nov", "Dec"],
        y=miscon
    ))
    fig.update_layout(
        title="Misconduct for " + sci + " " + year,
        xaxis_title="Month",
        yaxis_title="Misconduct count"
    )
    fig.show()

def sci_histogram(sci_miscon_rates, sci, global_mean, start_date, end_date):
    # Take dictionaries of SCI by month for population and misconduct.
    # TODO: fix vline and normalize x and y axis.
    #
    # Take dictionaries of SCI by month for population and misconduct.
    # TODO: fix vline and normalize x and y axis.
    # fig = go.Figure()
    # fig.add_trace(go.Histogram(x=list(sci_miscon_rates.values()), orientation='v'))
    counts, bins = np.histogram(list(sci_miscon_rates.values()))
    bins = 0.5 * (bins[:-1] + bins[1:])


    fig = px.bar(x=bins, y=counts, labels={'x': 'Monthly misconduct average rate', 'y': 'count'})
    mean = statistics.mean(list(sci_miscon_rates.values()))
    fig.add_vline(
        x=global_mean,
        line_width=2,
        line_dash='solid',
        line_color='orange',
        annotation={
            'font': {
                'size': 12,
                'family': 'Times New Roman',
                'color': 'black',
            }
        },
        annotation_text="Average rate across all SCIs",
        annotation_position='top right'
    )
    fig.add_vline(
        x=mean,
        line_width=2,
        line_dash='solid',
        line_color='green',
        annotation={
            'font': {
                'size': 12,
                'family': 'Times New Roman',
                'color': 'white',
            }
        },
        annotation_text="Average for " + sci,
        annotation_position='bottom right',
    )
    #
    fig.update_layout(
        title="Misconduct for " + sci + " " + start_date + " to " + end_date
    )

    return fig

def histogram_matplotlib(sci_miscon_rates, sci, global_mean, start_date, end_date):
    counts, bins = np.histogram(list(sci_miscon_rates.values()))
    pyplot.stairs(counts, bins)
    pyplot.hist(bins[:-1], bins, weights=counts)
    pyplot.show()