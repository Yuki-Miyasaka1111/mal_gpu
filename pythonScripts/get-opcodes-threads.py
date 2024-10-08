import os
import pandas as pd

# Initialize an empty dataframe to store combined data
combined_df = pd.DataFrame()

# Function to process each CSV file
def process_csv(input_csv):
    global combined_df
    
    # Read the CSV file into a dataframe
    df = pd.read_csv(input_csv)
    
    # Extract columns 'a' and 'b' and append to combined dataframe
    combined_df = combined_df.append(df[['Opcodes', 'Threads']], ignore_index=True)

# Function to iterate through all CSV files in a folder
def process_folder(folder_path):
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Process each CSV file
            process_csv(os.path.join(folder_path, filename))

# Specify the folder containing CSV files
folder_path = './Trojan'

# Process all CSV files in the specified folder
process_folder(folder_path)

# Save the combined dataframe to a new CSV file
combined_df.to_csv('combined_trojan_data.csv', index=False)
