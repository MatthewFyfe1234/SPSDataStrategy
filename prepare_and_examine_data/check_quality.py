import math
from prepare_and_examine_data import prepare_data as pd
from datetime import datetime

filename = 'C:\\Users\\Dell Precision\\PycharmProjects\\SewageTreatment\\sample_data.csv'
# Load data into dataframe
data = pd.load_data(filename)
# Remove duplicate instances and reindex
data = pd.dedupe_data(data)
clean_data = pd.remove_instances_where_x_column_is_null(data, 2)

# Some, fairly crude, checks on the data quality. Works for this small dataset
# Instances per station 'ID'
instance_counts_per_station = dict()
for valid_val in set(clean_data['ID']):
    for value in list(clean_data['ID']):
        if value == valid_val:
            instance_counts_per_station[valid_val] = instance_counts_per_station.get(valid_val, 0) + 1

# Check for invalid values in the 'Energy' column
missing_count_energy = 0
for value in list(data['Energy']):
    if math.isnan(value):
        missing_count_energy += 1
energy_values_nan_percent = round(missing_count_energy / len(data) * 100, 2)

# Check for invalid values in 'Observed Issue' column
valid_value_count_issues = 0
for value in list(clean_data['Observed_Issue']):
    for valid_val in [0, 1]:
        if value == valid_val:
            valid_value_count_issues += 1
valid_issue_level_percent = round(valid_value_count_issues / len(clean_data) * 100, 2)

# Instances per 'Date' (this is not a great way of checking for continuity)
date_set = list(set(clean_data['Date']))
date_set.sort(key=lambda date_: datetime.strptime(date_, "%m/%d/%Y"))
instance_counts_per_date = dict()
for date in date_set:
    for value in list(clean_data['Date']):
        if value == date:
            instance_counts_per_date[value] = instance_counts_per_date.get(value, 0) + 1

print(instance_counts_per_station)
print('Energy values missing (from original data-set): ' + str(energy_values_nan_percent) + '%')
print('Invalid or missing \'Observed issue\' values: ' + str(100 - valid_issue_level_percent) + '%')
print(instance_counts_per_date)
