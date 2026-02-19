# Main function for running data processing
from data_report import *
from misconduct import *
from population import *
from output_csv import *
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
                      DATE_START, DATE_END, './output')

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

    # cap = monthly_cap_in_range()
    # pop = monthly_pop_in_range()
    #miscs = monthly_miscon_in_range()
    #miscs_rate = monthly_miscon_rates()

    #print("output: ", output())

    # misconduct_controlled_counts = {}
    # misconduct_uncontrolled_counts = {}
    # for sci in scis():
    #     miscons = date_range_miscons()
    #     control, uncontrolled_count = check_control(miscons, sci)
    #     misconduct_uncontrolled_counts[sci] = uncontrolled_count
    #     misconduct_controlled_counts[sci] = len(control)
    # print("Controlled counts: ", misconduct_controlled_counts)
    # print("No controll counts: ", misconduct_uncontrolled_counts)

    total_miscon_check = {}
    miscons = date_range_miscons()
    year1 = miscon_per_institution( data_report('./data_files', MISCON), 2023)
    print("2023: ", year1)
    year2 = miscon_per_institution( data_report('./data_files', MISCON), 2024)
    for sci in scis():
        total_miscon_check[sci] = year1[sci]+year2[sci]

    print('total check: ', total_miscon_check)


    output_dict_no_hour_control= {'ALB': 5151, 'BEN': 3247, 'CBS': 898, 'CAM': 2922, 'CHS': 2091, 'COA': 4010, 'DAL': 3384,
                   'FYT': 3483, 'FRS': 5111, 'FRA': 1827, 'GRN': 4087, 'HOU': 3894, 'HUN': 5230, 'LAU': 1143,
                   'MAH': 3141, 'MER': 1000, 'MUN': 1843, 'PHX': 5899, 'PNG': 2833, 'QUE': 33, 'ROC': 3540, 'SMI': 2230,
                   'SMR': 4165, 'WAM': 914}

    controlled_counts_reduced_for_hour = {'ALB': 5554, 'BEN': 3415, 'CBS': 952, 'CAM': 3067, 'CHS': 2264, 'COA': 4246,
                                          'DAL': 3627, 'FYT': 3650, 'FRS': 5496, 'FRA': 1918, 'GRN': 4281, 'HOU': 4107,
                                          'HUN': 5589, 'LAU': 1195, 'MAH': 3355, 'MER': 1050,'MUN': 1960, 'PHX': 6244,
                                          'PNG': 3043, 'QUE': 36, 'ROC': 3748, 'SMI': 2329, 'SMR': 4462, 'WAM': 952}

    miscon_counts_not_controlled = {'ALB': 259380, 'BEN': 158048, 'CBS': 45496, 'CAM': 142956, 'CHS': 105732, 'COA': 196636,
                                    'DAL': 165220, 'FYT': 170500, 'FRS': 264308, 'FRA': 87736, 'GRN': 197384, 'HOU': 193204,
                                    'HUN': 258016, 'LAU': 55572, 'MAH': 154132, 'MER': 48884, 'MUN': 91520, 'PHX': 289696,
                                    'PNG': 144716, 'QUE': 1496, 'ROC': 173844, 'SMI': 105644, 'SMR': 206272, 'WAM': 43868}



    #
    # print("total misconduct count for 2023: ", miscon_by_year(data_report('./data_files', MISCON), '2023').size)
    # print("total misconduct count for 2024: ", miscon_by_year(data_report('./data_files', MISCON), '2024').size)
    print("Miscon sci list: ", scis_check())

    extra_miscon_scis = ['PIT', 'CRE', 'GRA', 'GRE', 'RET', 'WAY', '129', '756', '104', '136', '201', '117', '203', '116',
                         '131', '109', '102', '305', '106', '319', '124', '119', '225', '127', '209', '313', '135', '231',
                         '304', '303', '317', '204', '133', '126', '999']

    extra_counts = {'PIT': 0, 'CRE': 0, 'GRA': 0, 'GRE': 0, 'RET': 0, 'WAY': 0, '129': 0, '756': 0, '104': 0, '136': 0,
             '201': 0, '117': 0, '203': 0, '116': 0, '131': 0, '109': 0, '102': 0, '305': 0, '106': 0, '319': 0,
             '124': 0, '119': 0, '225': 0, '127': 0, '209': 0, '313': 0, '135': 0, '231': 0, '304': 0, '303': 0,
             '317': 0, '204': 0, '133': 0, '126': 0, '999': 0}


    # ex_misconduct_controlled_counts = {}
    # ex_misconduct_uncontrolled_counts = {}
    # miscons = date_range_miscons()
    # for sci in extra_miscon_scis:
    #     print("SCI: ", sci)
    #     control, uncontrolled_count = check_control(miscons, sci)
    #     ex_misconduct_uncontrolled_counts[sci] = uncontrolled_count
    #     ex_misconduct_controlled_counts[sci] = len(control)
    # print("Controlled counts: ", ex_misconduct_controlled_counts)
    # print("No controll counts: ", ex_misconduct_uncontrolled_counts)

    # main(function='histogram', SCI='ALB')
    #
    # main(function='scatter_plot')

    #main(function='form_141')

    #main(function='monthly_miscon')

