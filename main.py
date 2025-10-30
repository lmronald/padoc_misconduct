# Main function for running data processing
from data_report import *
from misconduct import *
from population import *
from visualization import *
from capacity import *
import os

def main(**kwargs):
    if 'date-start' in kwargs:
        DATE_START = kwargs['date-start']
    if 'date-end' in kwargs['date-end']:
        DATE_END = kwargs['date-end']
    if 'year' in kwargs:
        YEAR = kwargs['year']
    if 'miscon' in kwargs:
        MISCON = kwargs['miscon']
    if 'population' in kwargs:
        POP = kwargs['population']
    if 'capcaity' in kwargs:
        CAP = kwargs['capacity']
    if 'occupancy' in kwargs:
        OCC = kwargs['occupancy']
    if kwargs['function'] == 'annual_miscon_rates':
        annual_miscon_rates()
    if kwargs['function'] == 'histogram':
        histogram(kwargs['SCI'])
    if kwargs['function'] == 'scatter_plot':
        scatter_plot()
    if kwargs['function'] == 'form_141':
        form_141()
    if kwargs['function'] == 'monthly_miscon':
       print( monthly_miscon())

def annual_miscon_rates():
    inst_miscon_report = data_report('./', MISCON)
    misconduct = miscon_per_institution(inst_miscon_report, YEAR)

    inst_pop_report_annual = data_report('./', POP)
    population = population_per_institution(inst_pop_report_annual, YEAR)
    # Delete misformed inst.
    del population["WAM*"]
    return rates_of_misconduct_per_year(misconduct, population)


def monthly_miscon():
    inst_miscon_report_monthly = data_report('./', MISCON)
    scis = sci_list(inst_miscon_report_monthly, 'institution')
    return miscon_per_institution_by_month_and_year(inst_miscon_report_monthly, scis, YEAR)


def monthly_pop():
    inst_pop_report_monthly = data_report('./', POP)
    pop_by_month = population_per_institution_by_month_and_year(inst_pop_report_monthly, YEAR)
    # Delete misformed inst.
    del pop_by_month["WAM*"]
    return pop_by_month

def date_range_miscons():
    miscon_per_institution_in_date_range(data_report('./', MISCON), DATE_START, DATE_END)

def monthly_cap():
    inst_cap_report_monthly = data_report('./', CAP)
    return capacity_per_institution_by_month_and_year(inst_cap_report_monthly, YEAR)


def monthly_miscon_rates():
    return miscon_rates_by_month_and_year(monthly_miscon(), monthly_pop())


def scatter_plot():
    all_sci_scatter_plot(monthly_miscon_rates(), monthly_cap(), YEAR)


def histogram(sci):
    sci_histogram(monthly_miscon_rates()[sci], sci, YEAR)

def form_141():
    inst_miscon_report_monthly = data_report('./', MISCON)
    scis = sci_list(inst_miscon_report_monthly, 'institution')
    return form_141_counts(inst_miscon_report_monthly, scis, YEAR)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    """
    TODO: set up kwargs that take in year-range, data file, function, visualization-type
    ex: main.py FUNCTION YEAR MISCON POP CAP 
    
    TODO: create histogram based on frequency of misconducts per year by person instead
    of averages across institution??
    
    TODO: update year filtering to work for multiple years/range of years.
    """
    YEAR = '2023'
    DATE_START = '01-01-2023'
    DATE_END = '12-31-2024'
    MISCON = 'dbo_Miscon.txt'
    POP = 'physically-present-population-23-24.csv'
    CAP = 'occupancy-23-24.csv'
    OCC = 'occupancy-23-24.csv'

    date_range_miscons()

    #main(function='histogram', SCI='ALB')

    # main(function='scatter_plot')

    #main(function='form_141')

    #main(function='monthly_miscon')

