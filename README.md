# Schema Integrity & Data Report

## Data Source

The `used_data/` folder contains the 5 normalized tables used for the query competition:

- `world_cups.csv` — Tournament-level summary (22 World Cups, 1930–2022)
- `world_cup_matches.csv` — Match-level results across all World Cups
- `international_matches.csv` — International match results (friendlies, qualifiers, tournaments)
- `world_cup_players.csv` — Player squad details for the 2022 World Cup
- `world_cup_squads.csv` — Master dimension table of all 231 teams with FIFA rankings and federation assignments

## Referential Integrity

All foreign key relationships between tables are valid. Every child column value exists in its referenced parent column.

| Child Table | Child Column | → Parent Table | Parent Column | Status |
|---|---|---|---|---|
| world_cup_players | team | → world_cup_squads | team | ✅ VALID |
| world_cup_matches | home_team | → world_cup_squads | team | ✅ VALID |
| world_cup_matches | away_team | → world_cup_squads | team | ✅ VALID |
| international_matches | home_team | → world_cup_squads | team | ✅ VALID |
| international_matches | away_team | → world_cup_squads | team | ✅ VALID |
| world_cups | winner | → world_cup_squads | team | ✅ VALID |
| world_cups | runners_up | → world_cup_squads | team | ✅ VALID |
| world_cups | third | → world_cup_squads | team | ✅ VALID |
| world_cups | fourth | → world_cup_squads | team | ✅ VALID |
| world_cup_matches | year | → world_cups | year | ✅ VALID |

## Null Value Analysis

Only two columns across the entire schema contain null values. Both are expected and explained below.

| Table | Column | Missing Values | Reason |
|---|---|---|---|
| world_cup_squads | fifa_ranking | 199 | Only the 32 teams in the 2022 World Cup have FIFA rankings assigned. Historical and non-qualified teams are intentionally left as NULL. |
| world_cup_matches | win_conditions | 897 | Only populated when a match is decided by extra time, golden goal, or penalties. Standard results (wins/draws in regular time) are left as NULL. |
| international_matches | win_conditions | 17568 | Same as above — only populated for matches decided by penalties. |

## Validation Scripts

Two scripts in `script/` can be re-run at any time to verify the data condition:

- `script/referential_integrity_check.py` — Checks all foreign key relationships across tables
- `script/test_null.py` — Scans every column for null/missing values

To run on Windows (emoji support requires UTF-8):
```
set PYTHONUTF8=1 && python script\referential_integrity_check.py
python script\test_null.py
```

### Referential Integrity Output

```
Final Schema Referential Integrity Report
============================================================
Checking: world_cup_players.csv[team] -> world_cup_squads.csv[team]
  ✅ VALID: All child values exist in parent.

Checking: world_cup_matches.csv[home_team] -> world_cup_squads.csv[team]
  ✅ VALID: All child values exist in parent.

Checking: world_cup_matches.csv[away_team] -> world_cup_squads.csv[team]
  ✅ VALID: All child values exist in parent.

Checking: international_matches.csv[home_team] -> world_cup_squads.csv[team]
  ✅ VALID: All child values exist in parent.

Checking: international_matches.csv[away_team] -> world_cup_squads.csv[team]
  ✅ VALID: All child values exist in parent.

Checking: world_cups.csv[winner] -> world_cup_squads.csv[team]
  ✅ VALID: All child values exist in parent.

Checking: world_cups.csv[runners_up] -> world_cup_squads.csv[team]
  ✅ VALID: All child values exist in parent.

Checking: world_cups.csv[third] -> world_cup_squads.csv[team]
  ✅ VALID: All child values exist in parent.

Checking: world_cups.csv[fourth] -> world_cup_squads.csv[team]
  ✅ VALID: All child values exist in parent.

Checking: world_cup_matches.csv[year] -> world_cups.csv[year]
  ✅ VALID: All child values exist in parent.
```

### Null Value Check Output

```
Starting Null Value Check for Final Schema...
=============================================
Checking: world_cup_squads.csv...
  -> Status: NULLS DETECTED
     - fifa_ranking: 199 missing values

Checking: world_cups.csv...
  -> Status: CLEAN (0 null values found)

Checking: world_cup_players.csv...
  -> Status: CLEAN (0 null values found)

Checking: world_cup_matches.csv...
  -> Status: NULLS DETECTED
     - win_conditions: 897 missing values

Checking: international_matches.csv...
  -> Status: NULLS DETECTED
     - win_conditions: 17568 missing values
```
