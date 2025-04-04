import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
import os
import glob
from matplotlib.ticker import AutoMinorLocator, MultipleLocator

# Directories for CSV files and saving graphs
data_dir = 'data'
output_dir = 'graphs'
os.makedirs(output_dir, exist_ok=True)

# Get all CSV files in the data directory
csv_files = glob.glob(os.path.join(data_dir, '*.csv'))

# Function for linear approximation
def linear_func(x, a, b):
    return a * x + b

# Check that there are enough files for plotting
if len(csv_files) < 2:
    print("Необходимо минимум два CSV-файла для построения двух графиков.")
else:
    # Process the first two CSV files
    for i in range(2):
        file_path = csv_files[i]
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        # Read data from CSV file
        data = pd.read_csv(file_path, sep=';', decimal=',')

        # Column labels
        x_label = "f / f_0"
        xerr_label = "\sigma_{f/f_0}"
        y_label = "\phi_C / \pi"
        yerr_label = "\sigma_{\phi_C/pi}"

        # Extracting values
        x_data = data[x_label]
        y_data = data[y_label]
        y_err = data.get(yerr_label, None)
        x_err = data.get(xerr_label, None)

        # Least squares approximation
        params, params_covariance = curve_fit(linear_func, x_data, y_data)

        # Plot with error bars
        plt.errorbar(
            x_data, y_data,
            yerr=y_err, xerr=x_err,
            fmt='o', label=f'{file_name}', color=f'C{i}',
            ecolor='black', elinewidth=1, capsize=2,
            markersize=5, markeredgewidth=0.5, markerfacecolor='none'
        )

        # Plotting the fitted line
        x_fit = np.linspace(min(x_data), max(x_data), 100)
        y_fit = linear_func(x_fit, *params)
        # plt.plot(x_fit, y_fit, label=f'Fit {file_name}', color=f'C{i}', linestyle='--')

    # Set up the axis with ticks and minor grid
    
    plt.gca().xaxis.set_major_locator(MultipleLocator(0.02))
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator(5))
    plt.gca().yaxis.set_major_locator(MultipleLocator(0.1))
    plt.gca().yaxis.set_minor_locator(AutoMinorLocator(5))

    plt.minorticks_on()

    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Labels for the axes
    plt.xlabel(r'$f / f_0$')
    plt.ylabel(r'$\phi_C / \pi$')
    plt.legend()

    # Save the plot to a file
    output_file = f"{output_dir}/combined_graph.png"
    plt.savefig(output_file)
    plt.clf()  # Clear the figure for the next plot

    print(f"Graph saved as: {output_file}")
