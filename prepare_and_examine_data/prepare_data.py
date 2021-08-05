import pandas as pd
import math


class PrepareData:
    # Load data into dataframe
    def load_data(self, file):
        data = pd.read_csv(file, index_col=False)
        return data

    # Remove duplicate rows then reindex table
    def dedupe_data(self, data):
        data = data.drop(data.columns[0], axis=1)
        data = data.drop_duplicates()
        data.index = range(len(data))
        return data

    # Remove instances where a given column has missing values
    def remove_instances_where_var_k_is_nan(self, df, var_k):
        data = pd.DataFrame(columns=df.columns)
        for row in range(0, len(df)):
            if not math.isnan(df.iat[row, var_k]):
                entry = df.loc[df.index[row]]
                data = data.append([entry])
        data.index = range(len(data))
        return data
