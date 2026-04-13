# misconduct_controlled_counts = {}
# misconduct_uncontrolled_counts = {}
# miscons = date_range_miscons()
# for sci in scis():
#     control, uncontrolled_count = check_control(miscons, sci)
#     misconduct_uncontrolled_counts[sci] = uncontrolled_count
#     misconduct_controlled_counts[sci] = control
# print("Controlled counts: ", misconduct_controlled_counts)
# print("No controll counts: ", misconduct_uncontrolled_counts)


# out_path = './output'
# df_miscon = data_report('./data_files/', 'dbo_Miscon.txt')
# twenty_three = df_miscon[df_miscon['misconduct_date']// 10000 == 2023]
# twenty_four = df_miscon[df_miscon['misconduct_date']// 10000 == 2024]
#
# alb_th = twenty_three[twenty_three['institution'] == 'ALB'].shape[0]
# alb_fo = twenty_four[twenty_four['institution'] == 'ALB'].shape[0]
# print("ALB count: " ,alb_fo + alb_th)
#
# miscons = df_miscon[df_miscon['misconduct_date'] > 20221231]
# miscons_in_range = miscons[miscons['misconduct_date'] < 20250101]
# print("miscons shape: ", miscons_in_range.shape[0])
#
# miscon_per_inst_in_range_counts = {}
# for sci in scis():
#     miscons_in_range_sci = miscons_in_range.loc[miscons_in_range['institution'] == sci]
#     miscon_sci_subset = miscons_in_range_sci[['institution', 'misconduct_date', 'control_number']]
#     miscon_per_inst_in_range_counts[sci] = miscon_sci_subset.shape[0]
# print("miscon per inst: ", miscon_per_inst_in_range_counts)
# df = pd.DataFrame.from_dict(miscon_per_inst_in_range_counts, orient="index", columns=['SCI'])
# os.makedirs(out_path, exist_ok=True)
# df.to_csv(out_path + "/test.csv")

# print("Inst size: ", output_df.groupby('SCI').value_counts())
# sci_list = scis()
# total_count = {}
# count = 0
# miscons = date_range_miscons()
# for sci in sci_list:
#     sci_entries = output_df[output_df['SCI'] == sci]
#     sci_miscons = sci_entries[['Misconduct Count']]
#     #print("Sum: ", sci,  sci_miscons.cumsum())
#     control_repeats(miscons, sci)