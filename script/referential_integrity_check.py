import os
from typing import Dict, List, Set, Tuple

import pandas as pd

# Base folder where all CSV files live (same folder as this script)
FOLDER = os.path.dirname(os.path.abspath(__file__))

# Relationship Mapping: (Child File, Child FK Column, Parent File, Parent PK Column)
RELATIONSHIPS: List[Tuple[str, str, str, str]] = [
    ("2022_world_cup_squads.csv", "team", "2022_world_cup_groups.csv", "team"),
    ("2022_world_cup_matches.csv", "home_team", "2022_world_cup_groups.csv", "team"),
    ("2022_world_cup_matches.csv", "away_team", "2022_world_cup_groups.csv", "team"),
    ("world_cup_matches.csv", "home_team", "2022_world_cup_groups.csv", "team"),
    ("world_cup_matches.csv", "away_team", "2022_world_cup_groups.csv", "team"),
    ("international_matches.csv", "home_team", "2022_world_cup_groups.csv", "team"),
    ("international_matches.csv", "away_team", "2022_world_cup_groups.csv", "team"),
    ("world_cups.csv", "winner", "2022_world_cup_groups.csv", "team"),
    ("world_cups.csv", "runners_up", "2022_world_cup_groups.csv", "team"),
    ("world_cups.csv", "third", "2022_world_cup_groups.csv", "team"),
    ("world_cups.csv", "fourth", "2022_world_cup_groups.csv", "team"),
    ("world_cup_matches.csv", "year", "world_cups.csv", "year"),
    ("2022_world_cup_matches.csv", "year", "world_cups.csv", "year"),
]


def load_csv_cached(cache: Dict[str, pd.DataFrame], file_name: str) -> pd.DataFrame:
    """Load a CSV once and keep it in memory for subsequent checks."""
    if file_name in cache:
        return cache[file_name]

    file_path = os.path.join(FOLDER, file_name)

    # Read as string to avoid type mismatch issues (e.g., year int vs string).
    try:
        df = pd.read_csv(file_path, dtype=str, encoding="utf-8-sig", low_memory=False)
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, dtype=str, encoding="cp1252", low_memory=False)

    cache[file_name] = df
    return df


def normalize_series(series: pd.Series) -> pd.Series:
    """Normalize values by trimming spaces and removing blank-like entries."""
    cleaned = series.astype("string").str.strip()
    cleaned = cleaned.replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})
    return cleaned.dropna()


def normalize_column_name(name: str) -> str:
    """Convert column names to a comparable canonical form."""
    return "".join(ch for ch in name.lower() if ch.isalnum())


def resolve_column(df: pd.DataFrame, expected_name: str) -> str | None:
    """Find the real column in a dataframe using case/space/hyphen-insensitive matching."""
    expected_norm = normalize_column_name(expected_name)
    for col in df.columns:
        if normalize_column_name(str(col)) == expected_norm:
            return str(col)
    return None


def check_integrity() -> None:
    print("Referential Integrity Report")
    print("=" * 60)

    cache: Dict[str, pd.DataFrame] = {}

    for child_file, child_col, parent_file, parent_pk in RELATIONSHIPS:
        print(f"Checking: {child_file}[{child_col}] -> {parent_file}[{parent_pk}]")

        try:
            child_df = load_csv_cached(cache, child_file)
            parent_df = load_csv_cached(cache, parent_file)

            child_col_resolved = resolve_column(child_df, child_col)
            parent_pk_resolved = resolve_column(parent_df, parent_pk)

            if child_col_resolved is None:
                print(f"  ERROR: Column '{child_col}' not found in {child_file}\n")
                continue
            if parent_pk_resolved is None:
                print(f"  ERROR: Column '{parent_pk}' not found in {parent_file}\n")
                continue

            child_non_null = normalize_series(child_df[child_col_resolved])
            parent_non_null = normalize_series(parent_df[parent_pk_resolved])

            parent_values: Set[str] = set(parent_non_null.unique())
            missing_mask = ~child_non_null.isin(parent_values)

            missing_values_series = child_non_null[missing_mask]
            missing_count = int(missing_values_series.shape[0])
            orphan_unique = missing_values_series.drop_duplicates().tolist()

            if missing_count == 0:
                print("  VALID: All child values exist in parent.\n")
            else:
                print("  BROKEN")
                print(f"  Missing value count: {missing_count}")
                print(f"  First 5 orphan values: {orphan_unique[:5]}\n")

        except Exception as exc:
            print(f"  ERROR: Could not process relation. {exc}\n")


if __name__ == "__main__":
    check_integrity()
