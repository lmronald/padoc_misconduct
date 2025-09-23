# Main function for running data processing
from data_report import *
from misconduct import *
from population import *
import os

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    inst_miscon_report = data_report('./', 'dbo_Miscon.txt')
    misconduct = miscon_per_institution(inst_miscon_report, '2023')


    inst_pop_report_annual = data_report('./', 'physically-present-population-23-24.csv')
    population = population_per_institution(inst_pop_report_annual, '2023')
    annual_rates = rates_of_misconduct_per_year(misconduct, population)

    inst_miscon_report_monthly = data_report('./', 'dbo_Miscon.txt')
    miscon_by_month = miscon_per_institution_by_month_and_year(inst_miscon_report_monthly, '2023')
    print("miscon by month: ", miscon_by_month)

    inst_pop_report_monthly = data_report('./', 'physically-present-population-23-24.csv')
    pop_by_month = population_per_institution_by_month_and_year(inst_pop_report_monthly, '2023')
    print("pop by month: ", pop_by_month)
    #

