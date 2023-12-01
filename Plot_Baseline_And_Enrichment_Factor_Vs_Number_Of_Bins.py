'''
Plot_Baseline_And_Enrichment_Factor_Vs_Number_Of_Bins.py

Created: 11/29/2023 by Tom Lever
Updated: 11/29/2023 by Tom Lever

Plots a Decile-wise Lift Chart
'''

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

data_frame_of_observed_response_values_and_averages_and_standard_deviations_of_predicted_response_values = pd.read_csv('Data_Frame_Of_66289_Observed_Docking_Scores_And_Averages_And_Standard_Deviations_Of_Docking_Scores_Predicted_By_Bayesian_Model_Using_BART_Model_Based_On_Numbers_Of_Occurrences_Of_Substructures.csv')
data_frame_of_observed_response_values = data_frame_of_observed_response_values_and_averages_and_standard_deviations_of_predicted_response_values['observed_response_value']
tenth_percentile_of_observed_response_values = np.percentile(data_frame_of_observed_response_values, 10)
list_of_indicators_that_observed_response_value_belongs_to_lowest_10_percent = [1 if observed_response_value < tenth_percentile_of_observed_response_values else 0 for observed_response_value in data_frame_of_observed_response_values]
data_frame_of_observed_response_values_and_averages_and_standard_deviations_of_predicted_response_values_and_indicators_that_observed_response_value_belongs_to_lowest_10_percent = data_frame_of_observed_response_values_and_averages_and_standard_deviations_of_predicted_response_values.copy()
data_frame_of_observed_response_values_and_averages_and_standard_deviations_of_predicted_response_values_and_indicators_that_observed_response_value_belongs_to_lowest_10_percent['belongs_to_lowest_10_percent'] = list_of_indicators_that_observed_response_value_belongs_to_lowest_10_percent
column_belongs_to_lowest_10_percent = data_frame_of_observed_response_values_and_averages_and_standard_deviations_of_predicted_response_values_and_indicators_that_observed_response_value_belongs_to_lowest_10_percent['belongs_to_lowest_10_percent']
number_of_response_values_in_lowest_10_percent = sum(column_belongs_to_lowest_10_percent)
number_of_response_values = data_frame_of_observed_response_values_and_averages_and_standard_deviations_of_predicted_response_values_and_indicators_that_observed_response_value_belongs_to_lowest_10_percent.shape[0]
number_of_bins = 10
number_of_response_values_per_bin = number_of_response_values // number_of_bins
list_of_indices_of_bins = [i for i in range(0, number_of_bins)]
list_of_baselines = []

def append_baseline_or_enrichment_factor_to_list_of_baselines_or_enrichment_factors(data_frame, list_of_baselines_or_enrichment_factors):
    for i in list_of_indices_of_bins:
        lower_index_of_bin = number_of_response_values_per_bin * i
        upper_index_of_bin = number_of_response_values_per_bin * (i + 1) - 1
        bin = data_frame[lower_index_of_bin : upper_index_of_bin]
        column_belongs_to_lowest_10_percent_in_bin = bin['belongs_to_lowest_10_percent']
        number_of_response_values_in_bin_in_lowest_10_percent = sum(column_belongs_to_lowest_10_percent_in_bin)
        number_of_response_values_in_bin = bin.shape[0]
        baseline = (number_of_response_values_in_bin_in_lowest_10_percent / number_of_response_values_in_lowest_10_percent) / (number_of_response_values_in_bin / number_of_response_values)
        list_of_baselines_or_enrichment_factors.append(baseline)

append_baseline_or_enrichment_factor_to_list_of_baselines_or_enrichment_factors(data_frame_of_observed_response_values_and_averages_and_standard_deviations_of_predicted_response_values_and_indicators_that_observed_response_value_belongs_to_lowest_10_percent, list_of_baselines)
data_frame_of_observed_and_averaged_predicted_response_values_and_indicators_that_observation_belongs_to_lowest_10_percent_ordered_by_averaged_predicted_response_value = data_frame_of_observed_response_values_and_averages_and_standard_deviations_of_predicted_response_values_and_indicators_that_observed_response_value_belongs_to_lowest_10_percent.sort_values(by = 'average_of_predicted_response_values', ascending = True)
list_of_enrichment_factors = []
append_baseline_or_enrichment_factor_to_list_of_baselines_or_enrichment_factors(data_frame_of_observed_and_averaged_predicted_response_values_and_indicators_that_observation_belongs_to_lowest_10_percent_ordered_by_averaged_predicted_response_value, list_of_enrichment_factors)
data_frame_of_indices_of_bins_values_of_baselines_or_enrichment_factors_and_specifications_of_baselines_or_enrichment_factors = pd.DataFrame({
    'index of bin': list_of_indices_of_bins + list_of_indices_of_bins,
    'value of baseline or enrichment factor': list_of_baselines + list_of_enrichment_factors,
    'specification of baseline or enrichment factor': ['baseline' for _ in list_of_indices_of_bins] + ['enrichment factor' for _ in list_of_indices_of_bins]
})
sns.barplot(x = 'index of bin', y = 'value of baseline or enrichment factor', hue = 'specification of baseline or enrichment factor', data = data_frame_of_indices_of_bins_values_of_baselines_or_enrichment_factors_and_specifications_of_baselines_or_enrichment_factors)
plt.title('Value Of Baseline Or Enrichment Factor Vs. Index Of Bin\nFor Bayesian Neural Network And 1,060,613 Testing Observations')
plt.xticks(rotation = 90)
plt.show()