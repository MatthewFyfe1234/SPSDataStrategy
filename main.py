from prepare_and_examine_data import prepare_data
from prepare_and_examine_data import group_and_sort_data
from prepare_and_examine_data import visualise_data
from matplotlib.backends.backend_pdf import PdfPages
sd = group_and_sort_data.DataHelper()
pd = prepare_data.PrepareData()
vis = visualise_data.Visualisations()

filename = 'C:\\Users\\Dell Precision\\PycharmProjects\\SewageTreatment\\sample_data.csv'
# Load data into dataframe
data = pd.load_data(filename)
# Remove duplicate instances and reindex
data = pd.dedupe_data(data)
# Handle missing values
# Given the size of the data set and limited number of variables there is no way to sythesise missing 'Energy' values.
# Therefore, all instances where the energy data was missing were removed.
# No other variable had missing values (though whole instances were missing from the outset)
data = pd.remove_instances_where_var_k_is_nan(data, 2)
# Make individual tables for each station.
grouped_data = sd.group_data_to_dataframes_by_var_k_levels(data, 'ID')
# Get sorting order, by increasing 'Energy' mean
sorting_order = sd.get_table_sorting_order_by_var_k_mean_with_additional_variable(grouped_data, 0, 'Energy',
                                                                                  'Observed_Issue')

# Plot 'Energy' mean and 'Observed Issues' against station code.
energy_vs_issues = '\'Energy\' and \'Observed Issues\' Plotted Against Stations, Ordered by Increasing \'Energy\''
evi_x, evi_l, evi_r = 'Station Code', 'Days With Issues Over Month (%)', 'Average Daily Energy Usage (kWh)'
fig1 = vis.generate_plot_with_secondary_y(sorting_order, [0, 60], [0, 50], evi_x, evi_l, evi_r, energy_vs_issues)

# Get data for all stations identified to be within the zone with high risk of issues (identified in the plot above)
risk_zone_tables = sd.get_grouped_tables_within_mean_of_range_for_var_k(grouped_data, 'Energy', 4.2, 31.5)
# Get the ceoffecient of standard deviation for the identified 'risk_zone' stations
risk_zone_coeffs = sd.get_coefficient_of_standard_deviation_for_table_set_by_column_k(risk_zone_tables, 0, 'Energy')
# Order by increasing 'Energy'
risk_zone_coeffs.sort(key=lambda x: x[1])
# Plot the coefficient of standard deviation for all the stations within the risk zone
energy_vs_coeff_std_dev = '\'Energy\' and Coefficient of Standard Deviation Plotted Against Stations, Ordered by ' \
                          'Increasing \'Energy\''
evc_x, evc_l, evc_r = 'Station Code', 'Coeffiecient of Standard Deviation', 'Average Daily Energy Usage (kWh)'
fig2 = vis.generate_plot_with_secondary_y(risk_zone_coeffs, [0, 1.3], [0, 40],
                                          evc_x, evc_l, evc_r, energy_vs_coeff_std_dev)

# Plot daily 'Energy' for each station.
energy_variance = 'Visualising \'Energy\' Variability'
ev_x_var, ev_y_var, ev_x_name, ev_y_name = 'Date', 'Energy', 'Date', 'Energy (kWh)'
fig3 = vis.plot_array(5, 6, grouped_data, ev_x_var, ev_y_var, ev_x_name, ev_y_name, energy_variance)

# Make individual tables for stations where there were 'Observed Issues'.
plants_with_issues = sd.select_from_grouped_tables_by_value_inclusion(grouped_data, 3, 1)
# Order the stations with 'Observed Issues' by 'Energy' mean (within tuple).
plants_with_issues_energy_ordering = sd.get_table_sorting_order_by_var_k_mean_with_additional_variable(
    plants_with_issues, 0, 'Energy', 'Observed_Issue')
# Order station tables with 'Observed Issues' by mean 'Energy'.
ordered_issue_station_set = sd.order_grouped_df_set_by_tuple_set(plants_with_issues,
                                                                 plants_with_issues_energy_ordering)
# Make individual tables for '0' and '1' levels in 'Observed Issue' column, for each station.
nested_issue_sets = sd.split_table_set_by_var_k_levels(ordered_issue_station_set, 3)
# print(nested_issue_sets)
energy_range = 'Energy Boxplots for Stations with Issue\'s (in Order of Increasing \'Energy\' From Top Left to ' \
               'Bottom Right)'
x_levels = ['No Issues', 'Issues']
x_var, y_var, x_name, y_name = 'Observed_Issue', 'Energy', 'Observed Issue', 'Energy (kWh)'
fig4 = vis.level_boxplots_x_given_var_y(nested_issue_sets, ordered_issue_station_set, x_var, y_var, x_name, y_name,
                                        x_levels, energy_range)

# Plot all visuals to pdf
with PdfPages('Visuals.pdf') as pdf:
    for fig in [fig1, fig2, fig3, fig4]:
        pdf.savefig(fig)
