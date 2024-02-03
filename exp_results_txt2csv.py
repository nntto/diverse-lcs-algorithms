import re
from io import StringIO
import csv
import sys

# Redefining the function with all necessary regular expressions defined within its scope
def parse_experiment_data_fixed(data):
    # Regular expressions to extract the required data
    n_k_pattern = re.compile(r'n = .+? = (\d+), k = (\d+)')
    lcs_length_pattern = re.compile(r'lcs_length = (\d+)')
    lcs_count_pattern = re.compile(r'lcs_count = (\d+)')
    time_pattern = re.compile(r'(\d+\.\d+) real')
    memory_pattern = re.compile(r'(\d+)  maximum resident set size')
    algorithm_pattern = re.compile(r'Running (.+).py')

    # Splitting the data into lines for easier processing
    lines = data.split('\n')

    # Data structure to store the parsed data
    parsed_data = []

    for line in lines:
        # Extracting algorithm used
        algorithm_match = algorithm_pattern.search(line)
        if algorithm_match:
            algorithm = algorithm_match.group(1)
            continue

        # Extracting n and k values
        n_k_match = n_k_pattern.search(line)
        if n_k_match:
            n, k = n_k_match.groups()
            continue

        # Extracting LCS length
        lcs_length_match = lcs_length_pattern.search(line)
        if lcs_length_match:
            lcs_length = lcs_length_match.group(1)
            continue
            
        # Extracting LCS count
        lcs_count_match = lcs_count_pattern.search(line)
        if lcs_count_match:
            lcs_count = lcs_count_match.group(1)
            continue

        # Extracting running time
        time_match = time_pattern.search(line)
        if time_match:
            running_time = time_match.group(1)
            continue

        # Extracting memory usage
        memory_match = memory_pattern.search(line)
        if memory_match:
            memory_usage = memory_match.group(1)
            # Adding the extracted data to the list
            parsed_data.append({'algorithm': algorithm, 'n': n, 'k': k, 'lcs_length': lcs_length, 'lcs_count': lcs_count, 'running time': running_time, 'memory usage': memory_usage})

    return parsed_data

# filename from args
args = sys.argv[1:]
filename = args[0]

with open(filename, 'r') as f:
    experiment_data = f.read()

# Parsing the experiment data
parsed_experiment_data_fixed = parse_experiment_data_fixed(experiment_data)

# Creating a CSV from the parsed data
csv_output_fixed = StringIO()
csv_writer = csv.DictWriter(csv_output_fixed, fieldnames=['algorithm', 'n', 'k', 'lcs_length', 'lcs_count', 'running time', 'memory usage'])
csv_writer.writeheader()
csv_writer.writerows(parsed_experiment_data_fixed)

# Getting the CSV content as a string
csv_content_fixed = csv_output_fixed.getvalue()
csv_output_fixed.close()

# Displaying the first few lines of the CSV for review
print(csv_content_fixed)  # Displaying the first 500 characters to get an overview of the CSV content.

# output csv to file
with open('experiment_results.csv', 'w') as f:
    f.write(csv_content_fixed)