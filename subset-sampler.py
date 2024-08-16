import pandas as pd
import argparse
import numpy as np
import sys

def main(input_file, num_samples, output_file):
    try:
        # Read the input TSV file
        data = pd.read_csv(input_file, sep='\t')
        
        # Ensure the number of samples requested does not exceed the number of rows in the data
        if num_samples > len(data):
            print(f"Error: Number of samples requested ({num_samples}) exceeds the number of rows in the data ({len(data)})")
            sys.exit(1)
        
        # Uniformly sample rows without replacement
        sampled_data = data.sample(n=num_samples, random_state=1)
        
        # Write the sampled rows to the output TSV file
        sampled_data.to_csv(output_file, sep='\t', index=False)
    
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"Error: File '{input_file}' is empty.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Uniformly sample rows from a TSV file.')
    parser.add_argument('-i', '--input_file', type=str, required=True, help='Input TSV file')
    parser.add_argument('-n', '--num_samples', type=int, required=True, help='Number of rows to sample')
    parser.add_argument('-o', '--output_file', type=str, required=True, help='Output TSV file')
    
    args = parser.parse_args()
    
    # Check if the required arguments are provided
    if not args.input_file or not args.num_samples or not args.output_file:
        parser.print_help()
        sys.exit(1)
    
    main(args.input_file, args.num_samples, args.output_file)

