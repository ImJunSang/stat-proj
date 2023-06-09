from math import sqrt

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


files = {
    "namuwiki": pd.read_csv("./processed/namuwiki.csv"),
    "wikipedia": pd.read_csv("./processed/wikipedia.csv")
}

def count_outliers(values):
    q1, q3 = np.percentile(values, [25, 75])
    iqr = q3 - q1
    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)
    outliers = [x for x in values if x < lower_bound or x > upper_bound]
    return len(outliers)

def histogram(df, year, ax=None, axb=None, axbb=None,label=None):
    axb.set_title(f"{year}")

    column = year % 2010
    values = df.iloc[:, column]
    values.name = ""

    # Filter out rows with 0 or missing values
    mask = (values != 0) & (~np.isnan(values))
    values = values[mask]

    mean = values.mean()
    coef_var = sqrt(values.var()) / mean

    color = "blue" if label == "namuwiki" else "orange"
    outliners = count_outliers(values)

    if label == "namuwiki":
        ax.text(55, 65, f"Coef_var: {coef_var:.2f}, Outliner: {outliners}", color=color)
        sns.boxplot(x=values, ax=axb, color=color)
    else:
        ax.text(55, 55, f"Coef_var: {coef_var:.2f}, Outliner: {outliners}", color=color)
        sns.boxplot(x=values, ax=axbb, color=color)

    sns.histplot(values, kde=True, ax=ax, label=label, color=color)

fig2, ((axb0, axb1, axb2), (axbb0, axbb1, axbb2), (ax0, ax1, ax2), (_0, _1, _2),
       (axb3, axb4, axb5), (axbb3, axbb4, axbb5), (ax3, ax4, ax5)) = plt.subplots(7, 3, figsize=(12, 8), sharex=True, gridspec_kw={"height_ratios": (.05, .05, .39, .02, .05, .05, .39)})

for key in files:
    histogram(files[key], 2016, ax0, axb0, axbb0, key)
    histogram(files[key], 2017, ax1, axb1, axbb1, key)
    histogram(files[key], 2018, ax2, axb2, axbb2, key)
    histogram(files[key], 2019, ax3, axb3, axbb3, key)
    histogram(files[key], 2020, ax4, axb4, axbb4, key)
    histogram(files[key], 2021, ax5, axb5, axbb5, key)

for ax in [ax0, ax1, ax2, ax3, ax4, ax5]:
    ax.set_xlim(0, 200)
    ax.set_ylim(0, 100)
    ax.legend()

for ax in [_0, _1, _2]:
    ax.axis("off")

plt.show()