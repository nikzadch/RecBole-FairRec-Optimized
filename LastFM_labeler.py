# import numpy as np
import pandas as pd
import argparse

def load_data(file_path):
    # Load the data from a tab-separated CSV file
    data = pd.read_csv(file_path, sep='\t')
    return data

def compute_play_frequencies(play_counts):
    # Compute total plays for each user
    total_plays = play_counts.groupby('user_id:token')['rating:float'].sum().reset_index()
    total_plays.columns = ['user_id:token', 'total_play_count']
    
    # Merge total plays with play counts
    play_counts = play_counts.merge(total_plays, on='user_id:token')
    
    # Compute play frequency
    play_counts['play_frequency'] = play_counts['rating:float'] / play_counts['total_play_count']
    
    return play_counts

def rank_artists(play_counts):
    # Rank artists based on play frequency for each user
    play_counts['rank'] = play_counts.groupby('user_id:token')['play_frequency'].rank(ascending=False, method='first')
    
    return play_counts

def compute_cumulative_frequencies(play_counts):
    # Sort by user_id:token and rank to compute cumulative frequencies
    # play_counts = play_counts.sort_values(by=['user_id:token', 'rank'], ascending=[True, False])
    play_counts = play_counts.sort_values(by=['user_id:token', 'rank'])
    
    # Compute cumulative sum of frequencies for higher-ranked artists
    play_counts['cumulative_frequency'] = play_counts.groupby('user_id:token')['play_frequency'].cumsum() - play_counts['play_frequency']
    
    return play_counts

def estimate_ratings(play_counts):
    # Compute estimated ratings
    play_counts['estimated_rating:label'] = 4 * (1 - play_counts['cumulative_frequency'])
    
    # Apply the custom rounding function to the 'label:float' column
    play_counts['label:float'] = play_counts['estimated_rating:label'].apply(custom_round)
    
    return play_counts

# Function to round values according to the specified rules
def custom_round(x):
    # if x < 1:
    #     return 1
    # else:
    #     return int(round(x))
    return 1 if x < 1 else round(x)

def process_data(input_file, output_file):
    # Load data
    play_counts = load_data(input_file)
    
    # Step-by-step calculations
    play_counts = compute_play_frequencies(play_counts)
    play_counts = rank_artists(play_counts)
    play_counts = compute_cumulative_frequencies(play_counts)
    play_counts = estimate_ratings(play_counts)
    
    # Select the required columns
    result = play_counts[['user_id:token', 'item_id:token', 'name:token_seq', 'rating:float', 'play_frequency', 'rank', 'cumulative_frequency', 'estimated_rating:label', 'label:float']]
    
    # Save the result to the specified output file
    result.to_csv(output_file, sep='\t', index=False)
    
    # Optionally, print the result to the console (if desired)
    print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process LastFM dataset and estimate ratings.")
    parser.add_argument("input_file", help="Path to the input dataset file")
    parser.add_argument("-o", "--output-file", required=True, help="Path to the output file where results will be saved")
    
    args = parser.parse_args()
    
    # Process the data with the provided input and output file paths
    process_data(args.input_file, args.output_file)
