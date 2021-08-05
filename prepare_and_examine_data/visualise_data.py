import logging
import math
import sys
import warnings
import matplotlib.pyplot as plt


class Visualisations:
    if not sys.warnoptions:
        warnings.simplefilter('ignore')
    logging.getLogger().setLevel(logging.CRITICAL)

    def generate_plot_with_secondary_y(self, tuple_set, l_range, r_range, x_name, l_name, r_name, title):
        fig, ax1 = plt.subplots(figsize=(25, 25))
        fig.suptitle(title, ha='center')
        ax2 = ax1.twinx()
        ax1.bar(*zip(*[(x_var, y_var_r) for x_var, y_var_l, y_var_r in tuple_set]), color='r')
        ax1.set_xlabel(x_name)
        ax1.set_ylim(l_range)
        ax1.set_ylabel(l_name, color='r')
        ax2.plot(*zip(*[(x_var, y_var_l) for x_var, y_var_l, y_var_r in tuple_set]), 'b-')
        ax2.set_ylim(r_range)
        ax2.set_ylabel(r_name, color='b')
        ax1.set_xticklabels([x_var for x_var, y_var_l, y_var_r in tuple_set], rotation=90)
        return fig

    def plot_array(self, h_len, v_len, df_set, x_var, y_var, x_name, y_name, title):
        fig, axis = plt.subplots(v_len, h_len, figsize=(25, 25))
        fig.suptitle(title, ha='center')
        fig.text(0.5, 0.04, x_name, ha='center')
        fig.text(0.08, 0.5, y_name, va='center', rotation='vertical')
        for table in range(0, len(df_set)):
            sp_loc = axis[math.floor(table/h_len), table % h_len]
            sp_loc.bar(df_set[table][x_var], df_set[table][y_var])
            sp_loc.legend(title=df_set[table].iat[0, 0], framealpha=0.1, facecolor='blue')
            sp_loc.set_xticklabels(list(df_set[table][x_var]), rotation=45, fontsize=2)
        return fig

    # Plot array, with boxplots for different levels on same subplot.
    def level_boxplots_x_given_var_y(self, subgroups, groups, x_var, y_var, x_name, y_name, x_levels, title):
        fig, axis = plt.subplots(3, 3, figsize=(25, 25))
        fig.suptitle(title)
        fig.text(0.5, 0.04, x_name, ha='center')
        fig.text(0.09, 0.5, y_name, va='center', rotation='vertical')
        for pair in range(0, len(subgroups)):
            sp_loc = axis[math.floor(pair / 3), pair % 3]
            for table in range(0, len(subgroups[pair])):
                energy_arr = subgroups[pair][table][y_var]
                sp_loc.boxplot(energy_arr, positions=[(table + 0.5)/2])
            energy_arr, issue_arr = groups[pair][y_var], groups[pair][x_var]
            issue_percent = round(sum(list(issue_arr)) / len(groups[pair]) * 100, 1)
            sp_loc.legend(title=groups[pair].iat[0, 0] + '\n' + 'Issue %: ' + str(issue_percent),
                          framealpha=0.1, facecolor='blue')
            if pair >= 6:
                sp_loc.set_xticklabels(x_levels)
            else:
                sp_loc.set_xticklabels(['', ''])
        return fig
