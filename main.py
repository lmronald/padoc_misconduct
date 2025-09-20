# Main function for running data processing
from data_report import *
from misconduct import (miscon_per_institution)
from population import *
import os

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    inst_miscon_report = data_report('./', 'dbo_Miscon.txt')
    misconduct = miscon_per_institution(inst_miscon_report, '2023')

    inst_pop_report = data_report('./', 'physically-present-population-23-24.csv')
    population = population_per_institution(inst_pop_report, '2023')

    rates = rates_of_misconduct_per_year(misconduct, population)

