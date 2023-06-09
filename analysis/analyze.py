from math import sqrt

import pandas as pd
from pandas.core.frame import DataFrame
import numpy as np
from scipy.stats import linregress, ttest_ind
from scipy import integrate
import matplotlib.pyplot as plt
import seaborn as sns

from scalers import min_max_scaler, robust_scaler


files = {
    "namuwiki": pd.read_csv("./processed/namuwiki.csv"),
    "wikipedia": pd.read_csv("./processed/wikipedia.csv"),
    "korail": pd.read_csv("./processed/korail.csv")
}


def correlation(df_a: DataFrame, df_b: DataFrame, year):
    column = year % 2010
    a_values = df_a.iloc[:, column]
    b_values = df_b.iloc[:, column]

    # Filter out rows with 0 or missing values
    mask = (a_values != 0) & (b_values != 0) & (~np.isnan(a_values)) & (~np.isnan(b_values))
    a_values = a_values[mask]
    b_values = b_values[mask]

    correlation = a_values.corr(b_values)

    a_values_scaled = min_max_scaler(a_values)
    b_values_scaled = min_max_scaler(b_values)

    # 각 그룹 내 분산이 커서 F-test가 유의하지 않음
    # f_statistic, p_value = f_oneway(a_values_scaled, b_values_scaled)
    # print(f"{year}: F: {f_statistic:.2f}, P: {p_value:.4f}")

    slope, intercept, rvalue, pvalue, stderr = linregress(a_values_scaled, b_values_scaled)

    print(f"{year}: Corr: {correlation:.2f}, Y = {intercept:.2f} + {slope:.2f} * X, R: {rvalue:.2f}, P: {pvalue:.4f}, stderr: {stderr:.2f}")

    return correlation

def mean_variance(df, year, ax=None, label=None):
    column = year % 2010
    values = df.iloc[:, column]

    # Filter out rows with 0 or missing values
    mask = (values != 0) & (~np.isnan(values))
    values = values[mask]

    mean = values.mean()
    var = values.var()
    coef_var = sqrt(var) / mean

    print(f"{year},{mean:.2f},{var:.2f},{coef_var:.2f}")

    if ax and label in ["namuwiki", "wikipedia"]:
        sns.histplot(values, kde=True, ax=ax, label=label, stat='density', legend=True, color="blue" if label == "namuwiki" else "orange")

    return mean, var, coef_var

def gini(df, year):
    column = year % 2010
    values = df.iloc[:, column]
    values = values.sort_values()

    mask = (values != 0) & (~np.isnan(values))
    values = values[mask]
    
    n = len(values)
    x = np.linspace(0, 1, n)
    y = np.cumsum(values) / np.sum(values)
    lorenz_curve = np.column_stack((x, y))

    # Calculate the area under the Lorenz curve
    area_lorenz = integrate.simps(lorenz_curve[:, 1], lorenz_curve[:, 0])

    # Calculate the area under the line of perfect equality
    area_eq = 0.5

    # Calculate the Gini coefficient
    gini_coef = (area_eq - area_lorenz) / area_eq

    return gini_coef

years = list(range(2011, 2022))
years_recent = list(range(2011, 2023))
pairs = [("korail", "namuwiki"), ("korail", "wikipedia"), ("wikipedia", "namuwiki")]
means = {
    "namuwiki": [], 
    "wikipedia": [], 
    "korail": []
}
coef_vars = {
    "namuwiki": [], 
    "wikipedia": [], 
    "korail": []
}
ginis = {
    "namuwiki": [], 
    "wikipedia": [], 
    "korail": []
}
correlations = {
    "korail-namuwiki": [], 
    "korail-wikipedia": [], 
    "wikipedia-namuwiki": []
}

# fig1, axs = plt.subplots(3, 4, figsize=(12, 16))
fig2, (ax0, ax1, ax2, ax3) = plt.subplots(1, 4, figsize=(16, 4))

for key in files:
    print(f"{key[0].upper()}{key[1:]}")
    print("Mean, variance, coefficient of variance")
    for i, year in enumerate(years_recent):
        if year in [2022, 2023] and key == "korail":
            continue
        # mean, var, norm_var = mean_variance(files[key], year, axs[int(i / 4)][i % 4], key)
        mean, var, norm_var = mean_variance(files[key], year, None, key)
        means[key].append(mean)
        coef_vars[key].append(norm_var)

        gini_coef = gini(files[key], year)
        ginis[key].append(gini_coef)

for pair in pairs:
    file_a, file_b = pair
    print(f"Correlation between {file_a} and {file_b}")
    for year in years:
        corr = correlation(files[file_a], files[file_b], year)
        correlations[f"{file_a}-{file_b}"].append(corr)

t_stat_coef_var, p_value_coef_var = ttest_ind(coef_vars["namuwiki"], coef_vars["wikipedia"])
print(f"Coefficient of variance: t-statistic: {t_stat_coef_var:.2f}, p-value: {p_value_coef_var:.4f}")

t_stat_corr, p_value_corr = ttest_ind(correlations["korail-namuwiki"], correlations["korail-wikipedia"])
print(f"Correlation: t-statistic: {t_stat_corr:.2f}, p-value: {p_value_corr:.4f}")

t_stat_gini, p_value_gini = ttest_ind(ginis["namuwiki"], ginis["wikipedia"])
print(f"Gini coefficient: t-statistic: {t_stat_gini:.2f}, p-value: {p_value_gini:.4f}")

ax0.plot(years_recent, means["namuwiki"], label="Namuwiki")
ax0.plot(years_recent, means["wikipedia"], label="Wikipedia")
ax0.set_xlabel('Year')
ax0.set_ylabel('Mean')
ax0.set_title('Mean edit over time')
ax0.legend()

ax1.plot(years_recent, coef_vars["namuwiki"], label="Namuwiki")
ax1.plot(years_recent, coef_vars["wikipedia"], label="Wikipedia")
ax1.set_xlabel('Year')
ax1.set_ylabel('Coefficient of variation')
ax1.set_title('Coefficient of variation over time')
ax1.legend()

ax2.plot(years, ginis["namuwiki"][:11], label="Namuwiki")
ax2.plot(years, ginis["wikipedia"][:11], label="Wikipedia")
ax2.plot(years, ginis["korail"], label="Korail")
ax2.set_xlabel('Year')
ax2.set_ylabel('Gini coefficient')
ax2.set_title('Gini coefficient over time')
ax2.legend()

ax3.plot(years, correlations["korail-namuwiki"], label="Korail-Namuwiki")
ax3.plot(years, correlations["korail-wikipedia"], label="Korail-Wikipedia")
# ax3.plot(years, correlations["wikipedia-namuwiki"], label="Wikipedia-Namuwiki", color="green")
ax3.set_xlabel('Year')
ax3.set_ylabel('Correlation')
ax3.set_title('Correlation over time')
ax3.legend()

plt.show()