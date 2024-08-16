import pandas as pd
import argparse
import sys

def set_threshold(input_file, output_file, threshold, comparison):
    # Read the dataset
    data = pd.read_csv(input_file, sep="\t")
    
    # Drop ratings of zero
    data = data[data['rating:float'] != 0]
    
    # Add a new column "label:float" based on the threshold and comparison
    if comparison == 'ge':
        data['label:float'] = (data['rating:float'] >= threshold).astype(float)
    elif comparison == 'gt':
        data['label:float'] = (data['rating:float'] > threshold).astype(float)
    elif comparison == 'le':
        data['label:float'] = (data['rating:float'] <= threshold).astype(float)
    elif comparison == 'lt':
        data['label:float'] = (data['rating:float'] < threshold).astype(float)
    else:
        raise ValueError("Invalid comparison operator")

    # Save the processed dataset
    data.to_csv(output_file, index=False, sep="\t")

def parse_threshold(threshold_str):
    if threshold_str.startswith('--greater-or-equal='):
        return float(threshold_str.split('=')[1]), 'ge'
    elif threshold_str.startswith('--greater-than='):
        return float(threshold_str.split('=')[1]), 'gt'
    elif threshold_str.startswith('--lower-or-equal='):
        return float(threshold_str.split('=')[1]), 'le'
    elif threshold_str.startswith('--lower-than='):
        return float(threshold_str.split('=')[1]), 'lt'
    else:
        raise ValueError("Invalid threshold argument format")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process dataset to set threshold and add label column.')
    parser.add_argument('--threshold', type=str, required=True, help='Threshold for labeling with comparison operator (e.g., --greater-or-equal=3)')
    parser.add_argument('--dataset', type=str, required=True, help='Input dataset file')
    parser.add_argument('--output', type=str, default="processed_data.csv", help='Output dataset file')
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    try:
        threshold, comparison = parse_threshold(args.threshold)
    except ValueError as e:
        print(e)
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    set_threshold(args.dataset, args.output, threshold, comparison)
