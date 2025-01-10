import os
import re
import csv

# Define the directory path and pattern for log files
directory = "/home/keyvan/work/code-results-THESIS"
pattern = "Run_\d+_([a-zA-Z_]+)-([a-zA-Z0-9-]+)\.log"

# Define the output CSV file paths
output_test_file = "TESTresults.csv"
output_best_file = "BESTresults.csv"
output_combined_file = "results-comb.csv"

# Define the header for the CSV file
# header = [
#     "Method", "DataSet", "ndcg@5", "ndcg@10", "ndcg@15",
#     "recall@5", "recall@10", "recall@15",
#     "hit@5", "hit@10", "hit@15",
#     "mrr@5", "mrr@10", "mrr@15",
#     "precision@5", "precision@10", "precision@15",
#     "averagepopularity@5", "averagepopularity@10", "averagepopularity@15",
#     "itemcoverage@5", "itemcoverage@10", "itemcoverage@15",
#     "giniindex@5", "giniindex@10", "giniindex@15",
#     "Differential Fairness of sensitive attribute gender",
#     "Differential Fairness of sensitive attribute age",
#     "Value Unfairness of sensitive attribute gender",
#     "Value Unfairness of sensitive attribute age",
#     "Absolute Unfairness of sensitive attribute gender",
#     "Absolute Unfairness of sensitive attribute age",
#     "NonParity Unfairness of sensitive attribute gender",
#     "NonParity Unfairness of sensitive attribute age",
#     "Underestimation Unfairness of sensitive attribute gender",
#     "Underestimation Unfairness of sensitive attribute age",
#     "Overestimation Unfairness of sensitive attribute gender",
#     "Overestimation Unfairness of sensitive attribute age",
#     "tailpercentage@5", "tailpercentage@10", "tailpercentage@15",
#     "ndcg of sensitive attribute gender Men@5",
#     "ndcg of sensitive attribute gender Men@10",
#     "ndcg of sensitive attribute gender Men@15",
#     "ndcg of sensitive attribute gender Women@5",
#     "ndcg of sensitive attribute gender Women@10",
#     "ndcg of sensitive attribute gender Women@15",
#     "ndcg of sensitive attribute age YoungerGroup@5",
#     "ndcg of sensitive attribute age YoungerGroup@10",
#     "ndcg of sensitive attribute age YoungerGroup@15",
#     "ndcg of sensitive attribute age ElderGroup@5",
#     "ndcg of sensitive attribute age ElderGroup@10",
#     "ndcg of sensitive attribute age ElderGroup@15",
#     "Relative Difference of NDCG of sensitive attribute gender @5",
#     "Relative Difference of NDCG of sensitive attribute gender @10",
#     "Relative Difference of NDCG of sensitive attribute gender @15",
#     "Relative Difference of NDCG of sensitive attribute age @5",
#     "Relative Difference of NDCG of sensitive attribute age @10",
#     "Relative Difference of NDCG of sensitive attribute age @15",
#     "ndcg of sensitive subgroup Men YoungerGroup@5",
#     "ndcg of sensitive subgroup Men YoungerGroup@10",
#     "ndcg of sensitive subgroup Men YoungerGroup@15",
#     "ndcg of sensitive subgroup Men ElderGroup@5",
#     "ndcg of sensitive subgroup Men ElderGroup@10",
#     "ndcg of sensitive subgroup Men ElderGroup@15",
#     "ndcg of sensitive subgroup Women YoungerGroup@5",
#     "ndcg of sensitive subgroup Women YoungerGroup@10",
#     "ndcg of sensitive subgroup Women YoungerGroup@15",
#     "ndcg of sensitive subgroup Women ElderGroup@5",
#     "ndcg of sensitive subgroup Women ElderGroup@10",
#     "ndcg of sensitive subgroup Women ElderGroup@15",
#     "Variance of NDCG of sensitive attribute gender @5",
#     "Variance of NDCG of sensitive attribute gender @10",
#     "Variance of NDCG of sensitive attribute gender @15",
#     "ndcg of sensitive attribute age Young Adults@5",
#     "ndcg of sensitive attribute age Young Adults@10",
#     "ndcg of sensitive attribute age Young Adults@15",
#     "ndcg of sensitive attribute age Adults@5",
#     "ndcg of sensitive attribute age Adults@10",
#     "ndcg of sensitive attribute age Adults@15",
#     "ndcg of sensitive attribute age Teenager@5",
#     "ndcg of sensitive attribute age Teenager@10",
#     "ndcg of sensitive attribute age Teenager@15",
#     "ndcg of sensitive attribute age Seniors@5",
#     "ndcg of sensitive attribute age Seniors@10",
#     "ndcg of sensitive attribute age Seniors@15",
#     "Variance of NDCG of sensitive attribute age @5",
#     "Variance of NDCG of sensitive attribute age @10",
#     "Variance of NDCG of sensitive attribute age @15",
#     "ndcg of sensitive subgroup Men Young Adults@5",
#     "ndcg of sensitive subgroup Men Young Adults@10",
#     "ndcg of sensitive subgroup Men Young Adults@15",
#     "ndcg of sensitive subgroup Men Adults@5",
#     "ndcg of sensitive subgroup Men Adults@10",
#     "ndcg of sensitive subgroup Men Adults@15",
#     "ndcg of sensitive subgroup Men Teenager@5",
#     "ndcg of sensitive subgroup Men Teenager@10",
#     "ndcg of sensitive subgroup Men Teenager@15",
#     "ndcg of sensitive subgroup Men Seniors@5",
#     "ndcg of sensitive subgroup Men Seniors@10",
#     "ndcg of sensitive subgroup Men Seniors@15",
#     "ndcg of sensitive subgroup Women Young Adults@5",
#     "ndcg of sensitive subgroup Women Young Adults@10",
#     "ndcg of sensitive subgroup Women Young Adults@15",
#     "ndcg of sensitive subgroup Women Adults@5",
#     "ndcg of sensitive subgroup Women Adults@10",
#     "ndcg of sensitive subgroup Women Adults@15",
#     "ndcg of sensitive subgroup Women Teenager@5",
#     "ndcg of sensitive subgroup Women Teenager@10",
#     "ndcg of sensitive subgroup Women Teenager@15",
#     "ndcg of sensitive subgroup Women Seniors@5",
#     "ndcg of sensitive subgroup Women Seniors@10",
#     "ndcg of sensitive subgroup Women Seniors@15",
# ]

def extract_keys(file_path):
    header = ["Method", "DataSet"]
    
    with open(file_path, 'r') as file:
        for line in file:
            if "best valid" in line:
                result_line = line.split(":")[2].strip()
                best_valid_dict = dict(re.findall(r"'(.*?)', (.*?)\)", result_line))
                header = list(best_valid_dict.keys()) # Important to convert it to list lol
                break
                
    return header

# Replace 'input_file.txt' with the path to your input file
header = extract_keys('/home/keyvan/work/code-results-THESIS/Run_0234_ItemKNN-ml-1M.log')

# Initialize the result lists
results_test = []
results_best = []
results_combined = []

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

        # Find the lines with test and best valid results
        test_result_dict = {}
        best_valid_dict = {}
        combined_result_dict = {}
        for line in lines:
            if "test result" in line:
                result_line = line.split(":")[2].strip()
                test_result_dict = dict(re.findall(r"'(.*?)', (.*?)\)", result_line))
            if "best valid" in line:
                result_line = line.split(":")[2].strip()
                best_valid_dict = dict(re.findall(r"'(.*?)', (.*?)\)", result_line))
            if "best valid" in line or "valid result" in line:
                result_line = line.split(":")[2].strip()
                combined_result_dict = dict(re.findall(r"'(.*?)', (.*?)\)", result_line))

        # Add the results to the corresponding lists
        if test_result_dict:
            result_row = [method, dataset] + [test_result_dict.get(f, "-") for f in header[2:]]
            results_test.append(result_row)
        if best_valid_dict:
            result_row = [method, dataset] + [best_valid_dict.get(f, "-") for f in header[2:]]
            results_best.append(result_row)
        if combined_result_dict:
            result_row = [method, dataset] + [combined_result_dict.get(f, "-") for f in header[2:]]
            results_combined.append(result_row)

# Write the results to the output CSV files
with open(os.path.join(directory, output_test_file), "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(results_test)

with open(os.path.join(directory, output_best_file), "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(results_best)

with open(os.path.join(directory, output_combined_file), "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(results_combined)

print("Output CSV files created: " + output_test_file + ", " + output_best_file + " and " + output_combined_file)
