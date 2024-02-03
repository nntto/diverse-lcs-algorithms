import sys
import pandas as pd 
import matplotlib.pyplot as plt
import os


# filename from args
args = sys.argv[1:]
filename = args[0]

with open(filename, 'r') as f:
    experiment_data = f.read()

# Re-loading the CSV file into a DataFrame in case of any updates
df = pd.read_csv(filename)

# Convert running time and memory usage to numeric types for plotting
df['running time'] = pd.to_numeric(df['running time'], errors='coerce')
df['memory usage'] = pd.to_numeric(df['memory usage'], errors='coerce')

# Function to plot the graphs for specific k or n values with y-axis in logarithmic scale
def plot_experiment_data_log_scale(df, fixed_var, fixed_val, x_axis, y_axis):
    # Filtering the DataFrame for the specific value of k or n
    subset = df[df[fixed_var] == fixed_val]

    # Plotting separate lines for main and naive algorithms
    algorithms = subset['algorithm'].unique()
    for algorithm in algorithms:
        algorithm_subset = subset[subset['algorithm'] == algorithm]
        plt.plot(algorithm_subset[x_axis], algorithm_subset[y_axis], marker='o', label=algorithm)

    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.yscale('log')  # Setting y-axis to logarithmic scale
    plt.title(f'{y_axis} vs {x_axis} ({fixed_var} = {fixed_val}, Log Scale)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Function to plot the graphs for specific k or n values with y-axis in logarithmic scale and save the plots as images
def plot_and_save_experiment_data_log_scale(df, fixed_var, fixed_val, x_axis, y_axis):
    # Creating a directory to save the figures if it doesn't exist
    os.makedirs('./exp_plt', exist_ok=True)

    # Filtering the DataFrame for the specific value of k or n
    subset = df[df[fixed_var] == fixed_val]

    # Plotting separate lines for main and naive algorithms
    algorithms = subset['algorithm'].unique()
    
    # main -> 提案アルゴリズム，naive -> 素朴なアルゴリズム
    algorithm_map = {'main': 'proposed algorithm', 'naive': 'naive algorithm'}

    for algorithm in algorithms:
        algorithm_subset = subset[subset['algorithm'] == algorithm]
        # byte -> MB
        algorithm_subset.loc[:, 'memory usage'] = algorithm_subset['memory usage'] / 1024 / 1024

        plt.plot(algorithm_subset[x_axis], algorithm_subset[y_axis], marker='o', label=algorithm_map[algorithm])

    axis_map = {'n': 'n', 'k': 'k', 'lcs_count': 'lcs count', 'running time': 'running time [sec]', 'memory usage': 'maximum resident set size (MB)'}

    plt.xlabel(axis_map[x_axis])
    plt.ylabel(axis_map[y_axis])
    plt.yscale('log')  # Setting y-axis to logarithmic scale
    plt.xscale('log')  # Setting y-axis to logarithmic scale
    # plt.title(f'{y_axis} vs {x_axis} ({fixed_var} = {fixed_val}, Log Scale)')
    plt.legend()
    plt.grid(True)

    # Generating a filename for the plot
    filename = f'./exp_plt/{fixed_var}={fixed_val}_{x_axis}_vs_{y_axis}.pdf'.replace(' ', '_')
    plt.savefig(filename)  # Saving the plot as an image
    plt.close()  # Closing the plot to free up memory

    return filename

# Generating and saving the plots as images
filenames = []
for k in range(2, 11):
    filenames.append(plot_and_save_experiment_data_log_scale(df, 'k', k, 'n', 'running time'))
    filenames.append(plot_and_save_experiment_data_log_scale(df, 'k', k, 'n', 'memory usage'))
    filenames.append(plot_and_save_experiment_data_log_scale(df, 'k', k, 'lcs_count', 'running time'))
    filenames.append(plot_and_save_experiment_data_log_scale(df, 'k', k, 'lcs_count', 'memory usage'))

for n_i in range(1, 10):
    n = 9 * n_i
    filenames.append(plot_and_save_experiment_data_log_scale(df, 'n', n, 'k', 'running time'))
    filenames.append(plot_and_save_experiment_data_log_scale(df, 'n', n, 'k', 'memory usage'))
    filenames.append(plot_and_save_experiment_data_log_scale(df, 'n', n, 'lcs_count', 'running time'))
    filenames.append(plot_and_save_experiment_data_log_scale(df, 'n', n, 'lcs_count', 'memory usage'))