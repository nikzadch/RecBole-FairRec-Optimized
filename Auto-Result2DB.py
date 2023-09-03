import os
import re
import csv

# Define the directory path and pattern for log files
directory = "/home/keyvan/work/code-results"
pattern = r"Run_\d+_([a-zA-Z]+)-([a-zA-Z0-9-]+)\.log"

# Define the output CSV file path
output_file = "results.csv"

# Define the header for the CSV file
header = [
    "Method", "DataSet", "ndcg@5", "ndcg@10", "ndcg@15",
    "recall@5", "recall@10", "recall@15",
    "hit@5", "hit@10", "hit@15",
    "mrr@5", "mrr@10", "mrr@15",
    "precision@5", "precision@10", "precision@15",
    "averagepopularity@5", "averagepopularity@10", "averagepopularity@15",
    "itemcoverage@5", "itemcoverage@10", "itemcoverage@15",
    "giniindex@5", "giniindex@10", "giniindex@15",
    "Differential Fairness of sensitive attribute gender",
    "Differential Fairness of sensitive attribute age",
    "Value Unfairness of sensitive attribute gender",
    "Value Unfairness of sensitive attribute age",
    "Absolute Unfairness of sensitive attribute gender",
    "Absolute Unfairness of sensitive attribute age",
    "NonParity Unfairness of sensitive attribute gender",
    "NonParity Unfairness of sensitive attribute age",
    "Underestimation Unfairness of sensitive attribute gender",
    "Underestimation Unfairness of sensitive attribute age",
    "Overestimation Unfairness of sensitive attribute gender",
    "Overestimation Unfairness of sensitive attribute age",
    "tailpercentage@5", "tailpercentage@10", "tailpercentage@15",
    "Relative Difference of NDCG of sensitive attribute gender @5",
    "Relative Difference of NDCG of sensitive attribute gender @10",
    "Relative Difference of NDCG of sensitive attribute gender @15",
    "Relative Difference of NDCG of sensitive attribute age @5",
    "Relative Difference of NDCG of sensitive attribute age @10",
    "Relative Difference of NDCG of sensitive attribute age @15"
]

# Initialize the result list
results = []

# Iterate over the log files
for filename in os.listdir(os.path.expanduser(directory)):
    if filename.endswith(".log"):
        # Extract the Method and DataSet from the filename
        match = re.match(pattern, filename)
        if not match:
            continue

        method, dataset = match.group(1), match.group(2)

        # Read the log file
        with open(os.path.join(os.path.expanduser(directory), filename), "r") as file:
            lines = file.readlines()

        # Find the line with the best valid results
        result_dict = {}
        for line in lines:
            if "best valid" in line:
                # Extract the best valid results
                result_line = line.split(":")[2].strip()

                # Parse the result line into a dictionary
                result_dict = dict(re.findall(r"'(.*?)', (.*?)\)", result_line))

        # Add the results to the results list
        result_row = [method, dataset] + [result_dict.get(f, "-") for f in header[2:]]
        results.append(result_row)

# Write the results to the output CSV file
# with open(os.path.expanduser(output_file), "w", newline="") as file:
with open(os.path.join(directory, output_file), "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(results)

print("Output CSV file created: " + output_file)
