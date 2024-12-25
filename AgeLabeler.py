import pandas as pd
import argparse
import sys


def set_labels(input_file, output_file):
    # Read the dataset
    data = pd.read_csv(input_file, sep="\t")
    
    # Function to determine the age group label
    def age_group_label(age):
        if age < 20:
            return 'T'
        elif 20 <= age < 40:
            return 'Y'
        elif 40 <= age < 60:
            return 'A'
        else:
            return 'S'
    
    # Apply the function to the 'age:token' column
    data['age:token'] = data['age:token'].apply(age_group_label)

    # Save the processed dataset
    data.to_csv(output_file, index=False, sep="\t")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process dataset to set labels for separate age groups.')
    parser.add_argument('--dataset', type=str, required=True, help='Input dataset file')
    parser.add_argument('--output', type=str, default="processed_data.csv", help='Output dataset file')
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    try:
        set_labels(args.dataset, args.output)
    except ValueError as e:
        print(e)
        parser.print_help(sys.stderr)
        sys.exit(1)
    
