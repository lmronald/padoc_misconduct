from misconduct import *

def control_counts_per_institution_by_month_in_range(data_report, sci_list, start_date, end_date):
    # Creates a dictionary of the min, max, and mean control numbers per institution per month in date range.
    miscons_in_range = miscon_per_institution_in_date_range(data_report, start_date, end_date)
    start_year = start_date.year
    start_month = start_date.month
    end_year = end_date.year
    end_month = end_date.month
    data_for_range = miscons_in_range
    control_per_institution = {}
    for inst in sci_list:
        control_per_month = {}
        data_by_inst = data_for_range.loc[data_for_range['institution'] == inst]
        year = start_year
        while year != (end_year + 1):
            month = 1
            last_month = 12
            if year == start_year:
                month = start_month
            if year == end_year:
                last_month = end_month
            while month <= last_month:
                month_str = str(month)
                if month < 10:
                    month_str = "0" + month_str
                data_by_month = miscon_by_month_and_year(data_by_inst, month, year)
                control_per_month[month_str + '-' + str(year)] = control_repeats(data_by_month, inst)
                month += 1
            year += 1
        control_per_institution[inst] = control_per_month
    return control_per_institution


def control_repeats(data_report, sci):
    # Given a data report in the range, produce the mean, max, and min count for a given control number.
    # The min will most likely be 1 in all cases since we're not comparing to the list of controls outside of misconducts.
    scis_data = data_report.loc[data_report['institution'] == sci]
    mean_cont = scis_data[['institution', 'control_number']].control_number.value_counts().mean()
    max_cont = scis_data[['institution', 'control_number']].control_number.value_counts().max()
    min_cont = scis_data[['institution', 'control_number']].control_number.value_counts().min()
    return {'mean':mean_cont, 'max':max_cont, 'min':min_cont}