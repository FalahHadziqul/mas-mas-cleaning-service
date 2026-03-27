import pandas as pd
import os

# List of your specific CSV files
csv_files = [
    "2022_world_cup_groups.csv",
    "2022_world_cup_matches.csv",
    "2022_world_cup_squads.csv",
    "data_dictionary.csv",
    "international_matches.csv",
    "world_cup_matches.csv",
    "world_cups.csv"
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Try UTF-8 first, then common Windows/legacy encodings.
ENCODING_CANDIDATES = ["utf-8", "cp1252", "latin-1"]

def resolve_csv_path(filename):
    # Try common locations relative to this script.
    candidate_paths = [
        os.path.join(BASE_DIR, filename),
        os.path.join(BASE_DIR, "DATA", filename),
        os.path.join(BASE_DIR, "data", filename),
    ]

    for path in candidate_paths:
        if os.path.exists(path):
            return path

    # Return the default expected location for clearer error messages.
    return candidate_paths[0]

def read_csv_with_fallback(file_path):
    last_error = None

    for encoding in ENCODING_CANDIDATES:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            return df, encoding
        except UnicodeDecodeError as e:
            last_error = e

    raise last_error

def check_nulls_in_csv():
    print("Starting Null Value Check...\n" + "="*30)
    
    for file in csv_files:
        file_path = resolve_csv_path(file)
        print(f"Checking: {file}...")
        
        try:
            # Read the CSV with encoding fallback for non-UTF8 files.
            df, encoding_used = read_csv_with_fallback(file_path)
            if encoding_used != "utf-8":
                print(f"  -> Note: Loaded using {encoding_used} encoding")
            
            # Calculate nulls per column
            null_counts = df.isnull().sum()
            
            # Filter to only show columns that actually have nulls
            columns_with_nulls = null_counts[null_counts > 0]
            
            if columns_with_nulls.empty:
                print("  -> Status: CLEAN (0 null values found)\n")
            else:
                print("  -> Status: NULLS DETECTED")
                for col_name, count in columns_with_nulls.items():
                    print(f"     - {col_name}: {count} missing values")
                print() # Blank line for readability
                
        except FileNotFoundError:
            print(f"  -> ERROR: File not found at {file_path}. Please check your folder structure.\n")
        except Exception as e:
            print(f"  -> ERROR: Could not read file. Details: {e}\n")

if __name__ == "__main__":
    check_nulls_in_csv()