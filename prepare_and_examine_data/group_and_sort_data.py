import pandas as pd
from services import mathematical_services as ms


class DataHelper:
    def group_data_to_dataframes_by_var_k_levels(self, df, var_k):
        grouped_dataframes = []
        for group in list(set(df[var_k])):
            grouped_df = pd.DataFrame()
            for row in range(0, len(df)):
                if df.iat[row, 0] == group:
                    grouped_df = grouped_df.append(df.iloc[row])
            grouped_dataframes.append(grouped_df)
        return grouped_dataframes

    def get_grouped_tables_within_mean_of_range_for_var_k(self, df_set, var_k, range_min, range_max):
        valid_frames = []
        for table in df_set:
            mean_k = ms.MathematicalServices.mean(list(table[var_k]))
            if range_min < mean_k < range_max:
                valid_frames.append(table)
        return valid_frames

    def get_table_sorting_order_by_var_k_mean_with_additional_variable(self, grouped_tables, grouping_column, var_k, var_b):
        mean_table_sort = []
        for group in range(0, len(grouped_tables)):
            group_name = grouped_tables[group].iat[grouping_column, 0]
            mean_k = round(ms.MathematicalServices.mean(list(grouped_tables[group][var_k])), 2)
            issue_percent = round(sum(list(grouped_tables[group][var_b])) / len(grouped_tables[group]) * 100, 1)
            sorting_pair = (group_name, mean_k, issue_percent)
            mean_table_sort.append(sorting_pair)
        mean_table_sort.sort(key=lambda x: x[1])
        return mean_table_sort

    def get_coefficient_of_standard_deviation_for_table_set_by_column_k(self, df_set, identifier_col, var_k):
        coeff_set = []
        for group in df_set:
            id_ = group.iat[identifier_col, 0]
            mean_k = round(ms.MathematicalServices.mean(list(group[var_k])), 2)
            coeff = round(ms.MathematicalServices.coeff_of_std_deviation(group[var_k]), 2)
            coeff_set.append((id_, mean_k, coeff))
        return coeff_set

    def select_from_grouped_tables_by_value_inclusion(self, df_set, col_num, value):
        groups_with_value = []
        for group in df_set:
            append_group = False
            for row in range(0, len(group)):
                if group.iat[row, col_num] == value:
                    append_group = True
            if append_group:
                groups_with_value.append(group)
        return groups_with_value

    def order_grouped_df_set_by_tuple_set(self, df_set, tuple_set):
        reordered_dfs = []
        while len(reordered_dfs) != len(df_set):
            for table in df_set:
                if len(reordered_dfs) == len(df_set):
                    break
                if table.iat[0, 0] == tuple_set[len(reordered_dfs)][0]:
                    reordered_dfs.append(table)
        return reordered_dfs

    def split_table_set_by_var_k_levels(self, df_set, col_k_index):
        split_set = []
        level_set = list(set(df_set[0].iloc[:, col_k_index]))
        for table in df_set:
            subset = []
            for level in range(0, len(level_set)):
                level_df = pd.DataFrame(columns=df_set[0].columns)
                for row in range(0, len(table)):
                    if table.iat[row, col_k_index] == level_set[level]:
                        level_df = level_df.append(table.iloc[row])
                subset.append(level_df)
            split_set.append(subset)
        return split_set
