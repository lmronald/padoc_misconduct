import pandas as pd
import os
import re
import plotly.express as px
import plotly.graph_objects as go

"""
Graph visualizations of misconduct and population data across SCis.

Author: Lace Ronald
"""

def all_sci_scatter_plot(misconducts, populations, year):
    fig = go.Figure()
    for inst in populations:
        miscon_inst = misconducts[inst]
        pop_inst = populations[inst]
        sorted_miscon = sorted(miscon_inst)
        sorted_pop = sorted(pop_inst)
        miscon = [miscon_inst[key] for key in sorted_miscon]
        print("Miscon values: ", miscon)
        pop = [pop_inst[key] for key in sorted_pop]
        print("pop values: ", pop)
        fig.add_trace(go.Scatter(
            x=pop,
            y=miscon,
            mode="markers+text",
            name= inst + " " + year,
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

def sci_scatter_plot(sci_miscon, sci_population, sci, year):
    # Take dictionaries of SCI by month for population and misconduct.
    sorted_miscon = sorted(sci_miscon)
    sorted_pop = sorted(sci_population)
    miscon = [sci_miscon[key] for key in sorted_miscon]
    print("Miscon values: ", miscon)
    pop = [sci_population[key] for key in sorted_pop]
    print("pop values: ", pop)
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