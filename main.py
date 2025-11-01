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
    if 'date-end' in kwargs:
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

def scis():
    return sci_list(data_report('./', POP), 'Institution')

def annual_miscon_rates():
    inst_miscon_report = data_report('./', MISCON)
    misconduct = miscon_per_institution(inst_miscon_report, YEAR)

    inst_pop_report_annual = data_report('./', POP)
    population = population_per_institution(inst_pop_report_annual, scis(), YEAR)
    return rates_of_misconduct_per_year(misconduct, population)


def monthly_miscon():
    inst_miscon_report_monthly = data_report('./', MISCON)
    return miscon_per_institution_by_month_and_year(inst_miscon_report_monthly, scis(), YEAR)


def monthly_pop():
    inst_pop_report_monthly = data_report('./', POP)
    pop_by_month = population_per_institution_by_month_and_year(inst_pop_report_monthly, scis(), YEAR)
    return pop_by_month

def date_range_miscons():
    miscon_per_institution_in_date_range(data_report('./', MISCON), DATE_START, DATE_END)

def monthly_cap():
    inst_cap_report_monthly = data_report('./', CAP)
    return capacity_per_institution_by_month_and_year(inst_cap_report_monthly, scis(), YEAR)

def monthly_cap_in_range():
    inst_cap_report_monthly = data_report('./', CAP)
    return capacity_per_institution_by_month_in_range(inst_cap_report_monthly, scis(), DATE_START, DATE_END)

def monthly_miscon_rates():
    return miscon_rates_by_month_and_year(monthly_miscon(), monthly_pop())

def monthly_miscon_in_range():
    report = data_report('./', MISCON)
    return miscon_per_institution_by_month_in_range(report, scis(), DATE_START, DATE_END)

def monthly_pop_in_range():
    report = data_report('./', POP)
    return population_per_institution_by_month_in_range(report, scis(), DATE_START, DATE_END)

def scatter_plot():
    all_sci_scatter_plot(monthly_miscon_in_range(), monthly_cap_in_range(), YEAR)

def histogram(sci):
    sci_histogram(monthly_miscon_in_range()[sci], sci, YEAR)

def form_141():
    inst_miscon_report_monthly = data_report('./', MISCON)
    return form_141_counts(inst_miscon_report_monthly, scis(), YEAR)


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

    print("monthly miscon over two years: ", monthly_miscon_in_range())
    print("monthly pop over two years: ", monthly_pop_in_range())
    print("monthly cap over two years: ", monthly_cap_in_range())

    main(function='histogram', SCI='ALB')

    main(function='scatter_plot')

    #main(function='form_141')

    #main(function='monthly_miscon')

