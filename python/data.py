#%% INFO

# TITLE:       data.py
# DESCRIPTION: Import data into Spyder
# DATE:        2022-02-21

#%% PACKAGES
# Basics
import numpy as np  # NumPy offers comprehensive mathematical functions, random number generators, linear algebra routines, Fourier transforms, and more
from math import pi  # Mathematical library with values such as pi, e, etc.
import warnings  # This library is useful to be able to filter out groups of warnings.
import os  # The design of all built-in operating system dependent modules of Python

# Visualization
import pandas as pd  # pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language.
import matplotlib.pyplot as plt  # Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python.
import plotly as plot  # Plotly's Python graphing library makes interactive, publication-quality graphs.

#%% PREFERENCES
year = 2017
area = "NL01"

#%% CONSTANTS

#%% IMPORT
data_raw = pd.read_csv("movements.csv")  # Import data

#%% ANALYZE
global data_filtered  # Keep information available in all scripts

index_no = len(data_raw.index)  # Get number of rows
print("There are %d rows" % index_no)  # Print out the number of rows

col_names = list(data_raw.columns)  # Get column names
print("Column names are:")  # Print out text
print(*col_names, sep=", ")  # Print out column names

data_filtered = data_raw.loc[data_raw["year"] == year]  # Filter data by year
data_filtered = data_filtered.reset_index(drop=True)  # Reset index

unique_locations = pd.unique(
    data_filtered["area_from"]
)  # Get uniwue location values

area = unique_locations[0:3].tolist()
data_filtered = data_filtered[
    data_filtered["area_from"].isin(area)
]  # Filter data by area
data_filtered = data_filtered[
    data_filtered["area_to"].isin(area)
]  # Filter data by area

data_to = data_filtered.groupby(by=["area_to"])[
    "count"
].sum()  # DataFrame of count moved to
data_to = data_to.sort_index()  # Sort DataFrame

data_from = data_filtered.groupby(by=["area_from"])[
    "count"
].sum()  # DataFrame of count moved from
data_from = data_from.sort_index()  # Sort DataFrame

#%% MATPLOTLIB
move_to = data_filtered["area_to"].to_numpy()
move_from = data_filtered["area_from"].to_numpy()
move_count = data_filtered["count"].to_numpy()

# Scatter
plt.scatter(move_to, move_from, s=move_count / 100, alpha=0.5)
# plt.show()
plt.savefig("scatter.pdf")

# Bar
plt.bar(move_to, move_count)
# plt.show()
plt.savefig("bar.svg")

# Double bar
X = area
Y = data_to[area].tolist()
Z = data_from[area].tolist()

X_axis = np.arange(len(X))

plt.bar(X_axis - 0.2, Y, 0.4, label="Moved To", color="green")
plt.bar(X_axis + 0.2, Z, 0.4, label="Moved From", color="red")

plt.xticks(X_axis, X)
plt.xlabel("Municipality")
plt.ylabel("Number of people")
plt.title("Migration in and out of Municipalities")
plt.legend()
# plt.show()
plt.savefig("double bar.png")
