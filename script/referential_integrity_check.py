import os
import pandas as pd
from typing import Dict, List, Set, Tuple

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "used_data")

# Relationship Mapping: (Child File, Child FK Column, Parent File, Parent PK Column)
RELATIONSHIPS: List[Tuple[str, str, str, str]] = [
    # Players to Master Teams
    ("world_cup_players.csv", "team", "world_cup_squads.csv", "team"),
    
    # World Cup Matches to Master Teams
    ("world_cup_matches.csv", "home_team", "world_cup_squads.csv", "team"),
    ("world_cup_matches.csv", "away_team", "world_cup_squads.csv", "team"),
    
    # International Matches to Master Teams
    ("international_matches.csv", "home_team", "world_cup_squads.csv", "team"),
    ("international_matches.csv", "away_team", "world_cup_squads.csv", "team"),
    
    # Tournament Winners/Placements to Master Teams
    ("world_cups.csv", "winner", "world_cup_squads.csv", "team"),
    ("world_cups.csv", "runners_up", "world_cup_squads.csv", "team"),
    ("world_cups.csv", "third", "world_cup_squads.csv", "team"),
    ("world_cups.csv", "fourth", "world_cup_squads.csv", "team"),
    
    # Matches to World Cup Years
    ("world_cup_matches.csv", "year", "world_cups.csv", "year"),
]

def load_csv(file_path: str, cache: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    if file_path in cache:
        return cache[file_path]
    try:
        df = pd.read_csv(file_path, dtype=str, encoding="utf-8-sig")
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, dtype=str, encoding="cp1252")
    cache[file_path] = df
    return df


def normalize_column_name(name: str) -> str:
    return "".join(ch for ch in name.lower() if ch.isalnum())


def resolve_column(df: pd.DataFrame, expected_name: str) -> str | None:
    expected_norm = normalize_column_name(expected_name)
    for col in df.columns:
        if normalize_column_name(str(col)) == expected_norm:
            return str(col)
    return None

def check_integrity():
    print("Final Schema Referential Integrity Report")
    print("=" * 60)
    cache: Dict[str, pd.DataFrame] = {}

    for child_file, child_col, parent_file, parent_pk in RELATIONSHIPS:
        print(f"Checking: {child_file}[{child_col}] -> {parent_file}[{parent_pk}]")

        child_path = os.path.join(BASE_DIR, child_file)
        parent_path = os.path.join(BASE_DIR, parent_file)
        
        if not os.path.exists(child_path) or not os.path.exists(parent_path):
            print(f"  ERROR: Missing files for this relation.\n")
            continue

        child_df = load_csv(child_path, cache)
        parent_df = load_csv(parent_path, cache)

        child_col_resolved = resolve_column(child_df, child_col)
        parent_pk_resolved = resolve_column(parent_df, parent_pk)

        if child_col_resolved is None:
            print(f"  ERROR: Column '{child_col}' not found in {child_file}.\n")
            continue
        if parent_pk_resolved is None:
            print(f"  ERROR: Column '{parent_pk}' not found in {parent_file}.\n")
            continue

        # Normalize and find orphans
        child_values = set(child_df[child_col_resolved].astype(str).str.strip().replace({"": pd.NA, "nan": pd.NA, "None": pd.NA}).dropna().unique())
        parent_values = set(parent_df[parent_pk_resolved].astype(str).str.strip().replace({"": pd.NA, "nan": pd.NA, "None": pd.NA}).dropna().unique())
        
        orphans = child_values - parent_values

        if not orphans:
            print("  ✅ VALID: All child values exist in parent.\n")
        else:
            print(f"  ❌ BROKEN: {len(orphans)} orphan values found.")
            print(f"     Example Orphans: {list(orphans)[:5]}\n")

if __name__ == "__main__":
    check_integrity()