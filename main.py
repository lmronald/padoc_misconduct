# Main function for running data processing

from misconduct import (data_report, miscon_per_institution)
import os

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    report = data_report('./', 'dbo_Miscon.txt')
    print("Miscon opened")
    print(miscon_per_institution(report, '2020'))