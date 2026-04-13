# Main function for running data processing
from data_report import *
from misconduct import *
from population import *
from output_csv import *
from control_counts import *
from visualization import *
from capacity import *
import os
from datetime import datetime
from control_counts import *

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

def scis():
    return sci_list(data_report('./data_files', POP), 'Institution')

def scis_check():
    return sci_list(data_report('./data_files', MISCON), 'institution')

def annual_miscon_rates():
    inst_miscon_report = data_report('./data_files', MISCON)
    misconduct = miscon_per_institution(inst_miscon_report, YEAR)
    inst_pop_report_annual = data_report('./data_files', POP)
    population = population_per_institution(inst_pop_report_annual, scis(), YEAR)
    return rates_of_misconduct_per_year(misconduct, population)

def date_range_miscons():
    return miscon_per_institution_in_date_range(data_report('./data_files', MISCON), DATE_START, DATE_END)

def monthly_cap_in_range():
    inst_cap_report_monthly = data_report('./data_files', CAP)
    return capacity_per_institution_by_month_in_range(inst_cap_report_monthly, scis(), DATE_START, DATE_END)

def monthly_miscon_rates():
    return miscon_rates_by_month_and_year(monthly_miscon_in_range(), monthly_pop_in_range(), DATE_START, DATE_END)

def monthly_miscon_in_range():
    report = data_report('./data_files', MISCON)
    return miscon_per_institution_by_month_in_range(report, scis(), DATE_START, DATE_END)

def monthly_control_counts_in_range():
    report = data_report('./data_files', MISCON)
    return control_counts_per_institution_by_month_in_range(report, scis(), DATE_START, DATE_END)

def monthly_miscon_in_range_avg_rate():
    return average_rate(monthly_miscon_rates())

def monthly_pop_in_range():
    report = data_report('./data_files', POP)
    return population_per_institution_by_month_in_range(report, scis(), 'DOC Physically Present Total', DATE_START, DATE_END)

def monthly_ac_status():
    report = data_report('./data_files', POP)
    return population_per_institution_by_month_in_range(report, scis(), 'Restricted Housing AC', DATE_START, DATE_END)

def monthly_dc_status():
    report = data_report('./data_files', POP)
    return population_per_institution_by_month_in_range(report, scis(), 'Restricted Housing DC' , DATE_START, DATE_END)

def scatter_plot():
    all_sci_scatter_plot(monthly_miscon_in_range(), monthly_cap_in_range(), YEAR)

def histogram(sci):
    sci_histogram(monthly_miscon_rates()[sci], sci, monthly_miscon_in_range_avg_rate(), DATE_START, DATE_END)

def output():
    return output_csv(scis(), monthly_miscon_in_range(), monthly_miscon_rates(),
                      monthly_cap_in_range(), monthly_pop_in_range(), monthly_ac_status(), monthly_dc_status(),
                      monthly_control_counts_in_range(), DATE_START, DATE_END, './output')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    """
    TODO: set up kwargs that take in year-range, data file, function, visualization-type
    ex: main.py FUNCTION YEAR MISCON POP CAP 
    
    Currently: organizes data into monthly sets based on a range of dates, combines the miconduct data with population,
    capacity, and occupancy data into a CSV file in output. 
    """
    YEAR = '2023'
    DATE_START = datetime.datetime.strptime("20230101", "%Y%m%d")
    DATE_END = datetime.datetime.strptime("20241231", "%Y%m%d")
    MISCON = 'dbo_Miscon.txt'
    POP = 'physically-present-population-23-24.csv'
    CAP = 'occupancy-23-24.csv'
    OCC = 'occupancy-23-24.csv'

    print("output: ", output())

    output_df = data_report('./output', 'miscon_with_pop.csv')
    print(monthly_control_counts_in_range())









