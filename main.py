# Main function for running data processing

from misconduct import (data_report)
import os

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    report = data_report('./', 'dbo_Miscon.csv')
    print("Miscon opened")
    print(report)

