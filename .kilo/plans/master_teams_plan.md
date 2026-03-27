# Plan: Normalize CSV Headers + Create master_teams.csv

## Part 1: Normalize All CSV Headers to snake_case

Rename columns in every CSV file in-place. Mapping per file:

### 2022_world_cup_groups.csv
| Old | New |
|-----|-----|
| Group | group |
| Team | team |
| FIFA Ranking | fifa_ranking |

### 2022_world_cup_matches.csv
| Old | New |
|-----|-----|
| ID | id |
| Year | year |
| Date | date |
| Stage | stage |
| Home Team | home_team |
| Away Team | away_team |
| Host Team | host_team |

### world_cup_matches.csv
| Old | New |
|-----|-----|
| ID | id |
| Year | year |
| Date | date |
| Stage | stage |
| Home Team | home_team |
| Home Goals | home_goals |
| Away Goals | away_goals |
| Away Team | away_team |
| Win Conditions | win_conditions |
| Host Team | host_team |

### international_matches.csv
| Old | New |
|-----|-----|
| ID | id |
| Tournament | tournament |
| Date | date |
| Home Team | home_team |
| Home Goals | home_goals |
| Away Goals | away_goals |
| Away Team | away_team |
| Win Conditions | win_conditions |
| Home Stadium | home_stadium |

### world_cups.csv
| Old | New |
|-----|-----|
| Year | year |
| Host Country | host_country |
| Winner | winner |
| Runners-Up | runners_up |
| Third | third |
| Fourth | fourth |
| Goals Scored | goals_scored |
| Qualified Teams | qualified_teams |
| Matches Played | matches_played |

### world_cup_players.csv
| Old | New |
|-----|-----|
| ID | id |
| Team | team |
| Position | position |
| Name | name |
| Age | age |
| Caps | caps |
| Goals | goals |
| WC Goals | wc_goals |
| League | league |
| Club | club |

### data_dictionary.csv
Rename `Field` column values to match new snake_case names (e.g., `FIFA Ranking` -> `fifa_ranking`, `Runners-Up` -> `runners_up`, `WC Goals` -> `wc_goals`, etc.).

---

## Part 2: Create master_teams.csv

A single Python script (`create_master_teams.py`) that:

### Step 1 - Extract unique team names
Read these columns from each file (using new snake_case names):
- `2022_world_cup_groups.csv` -> `team`
- `2022_world_cup_matches.csv` -> `home_team`, `away_team`
- `world_cup_matches.csv` -> `home_team`, `away_team`
- `international_matches.csv` -> `home_team`, `away_team`
- `world_cups.csv` -> `winner`, `runners_up`, `third`, `fourth`

Union all values into a single sorted set.

### Step 2 - Left join FIFA rankings
From `2022_world_cup_groups.csv` (`team`, `fifa_ranking`). Non-2022 teams get NaN.

### Step 3 - Federation mapping
A dictionary of ~230 team-to-federation mappings covering:
- **CONMEBOL** (10): Argentina, Bolivia, Brazil, Chile, Colombia, Ecuador, Paraguay, Peru, Uruguay, Venezuela
- **CONCACAF** (~35): USA, United States, Mexico, Canada, Costa Rica, Honduras, Jamaica, Panama, Trinidad and Tobago, Haiti, Cuba, Guatemala, El Salvador, Nicaragua, and Caribbean/central nations
- **UEFA** (~55): All European nations + England, Scotland, Wales, Northern Ireland, plus historical: Soviet Union, Yugoslavia, Czechoslovakia, East Germany, German DR, Germany FR, Saarland
- **CAF** (~54): All African nations
- **AFC** (~47): All Asian nations + Australia
- **OFC** (~13): Pacific island nations + New Zealand
- **Historical/non-FIFA**: Regional teams (Andalusia, Basque Country, Brittany, etc.) -> 'Unknown'; Manchukuo -> 'Unknown'

### Step 4 - Export
Columns: `team_name`, `fifa_ranking`, `federation`. No index.

---

## File Structure

A single script `create_master_teams.py` that:
1. Renames headers in all 7 CSV files (Part 1)
2. Builds and exports `master_teams.csv` (Part 2)
