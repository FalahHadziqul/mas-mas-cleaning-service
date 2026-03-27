import pandas as pd
import os

# Updated list of final schema CSV files
csv_files = [
    "world_cup_squads.csv",
    "world_cups.csv",
    "world_cup_players.csv",
    "world_cup_matches.csv",
    "international_matches.csv"
]

# Resolve files from /data/used_data regardless of current working directory.
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "used_data")

def check_nulls_in_csv():
    print("Starting Null Value Check for Final Schema...\n" + "="*45)
    
    for file in csv_files:
        print(f"Checking: {file}...")
        file_path = os.path.join(BASE_DIR, file)
        
        try:
            # Load with fallback for potential encoding quirks
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, encoding='cp1252')
            
            # Calculate nulls per column
            null_counts = df.isnull().sum()
            columns_with_nulls = null_counts[null_counts > 0]
            
            if columns_with_nulls.empty:
                print("  -> Status: CLEAN (0 null values found)\n")
            else:
                print("  -> Status: NULLS DETECTED")
                for col_name, count in columns_with_nulls.items():
                    print(f"     - {col_name}: {count} missing values")
                print() 
                
        except FileNotFoundError:
            print(f"  -> ERROR: {file} not found at {file_path}.\n")
        except Exception as e:
            print(f"  -> ERROR: Could not read {file}. Details: {e}\n")

if __name__ == "__main__":
    check_nulls_in_csv()