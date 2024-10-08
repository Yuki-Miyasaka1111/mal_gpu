import os
import pandas as pd
import csv

# Function to count non-zero values in a specific column
def count_non_zero_rows_in_column(df, column_name):
    return df[column_name].astype(bool).sum()

# Path to the parent folder containing all the folders with CSV files
folder_path = './Trojan'

# Dictionary to store counts for each column
column_counts = {}

# Iterate over each CSV file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        
        # Read CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Iterate over each column
        for column_name in df.columns:
            if column_name not in column_counts:
                column_counts[column_name] = 0
            
            # Count rows with non-zero values in the column
            
            #count = count_non_zero_rows_in_column(df, column_name)
                #only count if threads is not 0
            count = df[(df['Threads'] != 0) & (df[column_name] != 0)][column_name].count()
            column_counts[column_name] += count

# Write the counts to a CSV file
output_file = 'trojan_column_counts.csv'
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Column Name', 'Count of Non-zero Values'])
    for column_name, count in column_counts.items():
        writer.writerow([column_name, count])

print(f"Results written to '{output_file}'")