import arviz
import pymc

inference_data_with_samples_from_posterior_probability_density_distribution_statistics_of_sampling_run_and_copy_of_observed_data = arviz.from_netcdf('Inference_Data.netcdf4')
rhat_values = pymc.stats.rhat(inference_data_with_samples_from_posterior_probability_density_distribution_statistics_of_sampling_run_and_copy_of_observed_data)
print(max(rhat_values.mu))