import pandas as pd

# =============================================================================
# PART 1: Normalize all CSV headers to snake_case
# =============================================================================

# Column rename mappings per file
HEADER_MAPS = {
    "2022_world_cup_groups.csv": {
        "Group": "group",
        "Team": "team",
        "FIFA Ranking": "fifa_ranking",
    },
    "2022_world_cup_matches.csv": {
        "ID": "id",
        "Year": "year",
        "Date": "date",
        "Stage": "stage",
        "Home Team": "home_team",
        "Away Team": "away_team",
        "Host Team": "host_team",
    },
    "world_cup_matches.csv": {
        "ID": "id",
        "Year": "year",
        "Date": "date",
        "Stage": "stage",
        "Home Team": "home_team",
        "Home Goals": "home_goals",
        "Away Goals": "away_goals",
        "Away Team": "away_team",
        "Win Conditions": "win_conditions",
        "Host Team": "host_team",
    },
    "international_matches.csv": {
        "ID": "id",
        "Tournament": "tournament",
        "Date": "date",
        "Home Team": "home_team",
        "Home Goals": "home_goals",
        "Away Goals": "away_goals",
        "Away Team": "away_team",
        "Win Conditions": "win_conditions",
        "Home Stadium": "home_stadium",
    },
    "world_cups.csv": {
        "Year": "year",
        "Host Country": "host_country",
        "Winner": "winner",
        "Runners-Up": "runners_up",
        "Third": "third",
        "Fourth": "fourth",
        "Goals Scored": "goals_scored",
        "Qualified Teams": "qualified_teams",
        "Matches Played": "matches_played",
    },
    "world_cup_players.csv": {
        "ID": "id",
        "Team": "team",
        "Position": "position",
        "Name": "name",
        "Age": "age",
        "Caps": "caps",
        "Goals": "goals",
        "WC Goals": "wc_goals",
        "League": "league",
        "Club": "club",
    },
    "data_dictionary.csv": {
        "Table": "table",
        "Field": "field",
        "Description": "description",
    },
}

# Also update the Field values inside data_dictionary.csv to match new snake_case names
FIELD_VALUE_MAP = {
    "Group": "group",
    "Team": "team",
    "FIFA Ranking": "fifa_ranking",
    "ID": "id",
    "Year": "year",
    "Date": "date",
    "Stage": "stage",
    "Home Team": "home_team",
    "Away Team": "away_team",
    "Host Team": "host_team",
    "Home Goals": "home_goals",
    "Away Goals": "away_goals",
    "Win Conditions": "win_conditions",
    "Tournament": "tournament",
    "Home Stadium": "home_stadium",
    "Host Country": "host_country",
    "Winner": "winner",
    "Runners-Up": "runners_up",
    "Third": "third",
    "Fourth": "fourth",
    "Goals Scored": "goals_scored",
    "Qualified Teams": "qualified_teams",
    "Matches Played": "matches_played",
    "Position": "position",
    "Name": "name",
    "Player": "name",
    "Age": "age",
    "Caps": "caps",
    "Goals": "goals",
    "WC Goals": "wc_goals",
    "League": "league",
    "Club": "club",
}

for filename, col_map in HEADER_MAPS.items():
    df = pd.read_csv(filename)
    df.rename(columns=col_map, inplace=True)

    # Special handling: update Field values in data_dictionary.csv
    if filename == "data_dictionary.csv":
        df["field"] = df["field"].map(FIELD_VALUE_MAP).fillna(df["field"])

    df.to_csv(filename, index=False)
    print(f"Normalized headers: {filename}")

print("\n--- Part 1 complete: All headers normalized ---\n")

# =============================================================================
# PART 2: Create master_teams.csv
# =============================================================================

# --- Step 1: Extract unique team names ---

teams = set()

df = pd.read_csv("2022_world_cup_groups.csv")
teams.update(df["team"].dropna().unique())

df = pd.read_csv("2022_world_cup_matches.csv")
teams.update(df["home_team"].dropna().unique())
teams.update(df["away_team"].dropna().unique())

df = pd.read_csv("world_cup_matches.csv")
teams.update(df["home_team"].dropna().unique())
teams.update(df["away_team"].dropna().unique())

df = pd.read_csv("international_matches.csv")
teams.update(df["home_team"].dropna().unique())
teams.update(df["away_team"].dropna().unique())

df = pd.read_csv("world_cups.csv")
for col in ["winner", "runners_up", "third", "fourth"]:
    teams.update(df[col].dropna().unique())

master = pd.DataFrame({"team_name": sorted(teams)})
print(f"Unique teams extracted: {len(master)}")

# --- Step 2: Left join FIFA rankings ---

groups = pd.read_csv("2022_world_cup_groups.csv")[["team", "fifa_ranking"]]
groups.rename(columns={"team": "team_name"}, inplace=True)

master = master.merge(groups, on="team_name", how="left")
print("FIFA rankings joined")

# --- Step 3: Federation mapping ---

FEDERATION_MAP = {
    # CONMEBOL
    "Argentina": "CONMEBOL",
    "Bolivia": "CONMEBOL",
    "Brazil": "CONMEBOL",
    "Chile": "CONMEBOL",
    "Colombia": "CONMEBOL",
    "Ecuador": "CONMEBOL",
    "Paraguay": "CONMEBOL",
    "Peru": "CONMEBOL",
    "Uruguay": "CONMEBOL",
    "Venezuela": "CONMEBOL",

    # CONCACAF
    "USA": "CONCACAF",
    "United States": "CONCACAF",
    "Mexico": "CONCACAF",
    "Canada": "CONCACAF",
    "Costa Rica": "CONCACAF",
    "Honduras": "CONCACAF",
    "Jamaica": "CONCACAF",
    "Panama": "CONCACAF",
    "Trinidad and Tobago": "CONCACAF",
    "Haiti": "CONCACAF",
    "Cuba": "CONCACAF",
    "Guatemala": "CONCACAF",
    "El Salvador": "CONCACAF",
    "Nicaragua": "CONCACAF",
    "Antigua and Barbuda": "CONCACAF",
    "Aruba": "CONCACAF",
    "Barbados": "CONCACAF",
    "Belize": "CONCACAF",
    "Bermuda": "CONCACAF",
    "Cayman Islands": "CONCACAF",
    "Curaçao": "CONCACAF",
    "Dominica": "CONCACAF",
    "Dominican Republic": "CONCACAF",
    "French Guiana": "CONCACAF",
    "Grenada": "CONCACAF",
    "Guadeloupe": "CONCACAF",
    "Guyana": "CONCACAF",
    "Martinique": "CONCACAF",
    "Puerto Rico": "CONCACAF",
    "Saint Kitts and Nevis": "CONCACAF",
    "Saint Lucia": "CONCACAF",
    "Saint Vincent and the Grenadines": "CONCACAF",
    "Suriname": "CONCACAF",
    "United States Virgin Islands": "CONCACAF",
    "Bahamas": "CONCACAF",

    # UEFA
    "Albania": "UEFA",
    "Andorra": "UEFA",
    "Armenia": "UEFA",
    "Austria": "UEFA",
    "Azerbaijan": "UEFA",
    "Belarus": "UEFA",
    "Belgium": "UEFA",
    "Bosnia and Herzegovina": "UEFA",
    "Bulgaria": "UEFA",
    "Croatia": "UEFA",
    "Cyprus": "UEFA",
    "Czech Republic": "UEFA",
    "Denmark": "UEFA",
    "England": "UEFA",
    "Estonia": "UEFA",
    "Faroe Islands": "UEFA",
    "Finland": "UEFA",
    "France": "UEFA",
    "Georgia": "UEFA",
    "Germany": "UEFA",
    "Gibraltar": "UEFA",
    "Greece": "UEFA",
    "Hungary": "UEFA",
    "Iceland": "UEFA",
    "Republic of Ireland": "UEFA",
    "Israel": "UEFA",
    "Italy": "UEFA",
    "Kazakhstan": "UEFA",
    "Kosovo": "UEFA",
    "Latvia": "UEFA",
    "Liechtenstein": "UEFA",
    "Lithuania": "UEFA",
    "Luxembourg": "UEFA",
    "Malta": "UEFA",
    "Moldova": "UEFA",
    "Montenegro": "UEFA",
    "Netherlands": "UEFA",
    "Northern Ireland": "UEFA",
    "North Macedonia": "UEFA",
    "Norway": "UEFA",
    "Poland": "UEFA",
    "Portugal": "UEFA",
    "Romania": "UEFA",
    "Russia": "UEFA",
    "San Marino": "UEFA",
    "Scotland": "UEFA",
    "Serbia": "UEFA",
    "Slovakia": "UEFA",
    "Slovenia": "UEFA",
    "Spain": "UEFA",
    "Sweden": "UEFA",
    "Switzerland": "UEFA",
    "Turkey": "UEFA",
    "Ukraine": "UEFA",
    "Wales": "UEFA",
    # Historical UEFA teams
    "Soviet Union": "UEFA",
    "Yugoslavia": "UEFA",
    "Czechoslovakia": "UEFA",
    "East Germany": "UEFA",
    "German DR": "UEFA",
    "Germany FR": "UEFA",
    "Saarland": "UEFA",
    "Serbia and Montenegro": "UEFA",

    # CAF
    "Algeria": "CAF",
    "Angola": "CAF",
    "Benin": "CAF",
    "Botswana": "CAF",
    "Burkina Faso": "CAF",
    "Burundi": "CAF",
    "Cameroon": "CAF",
    "Cape Verde": "CAF",
    "Central African Republic": "CAF",
    "Chad": "CAF",
    "Comoros": "CAF",
    "Congo": "CAF",
    "DR Congo": "CAF",
    "Djibouti": "CAF",
    "Egypt": "CAF",
    "Equatorial Guinea": "CAF",
    "Eritrea": "CAF",
    "Eswatini": "CAF",
    "Ethiopia": "CAF",
    "Gabon": "CAF",
    "Gambia": "CAF",
    "Ghana": "CAF",
    "Guinea": "CAF",
    "Guinea-Bissau": "CAF",
    "Ivory Coast": "CAF",
    "Kenya": "CAF",
    "Lesotho": "CAF",
    "Liberia": "CAF",
    "Libya": "CAF",
    "Madagascar": "CAF",
    "Malawi": "CAF",
    "Mali": "CAF",
    "Mauritania": "CAF",
    "Mauritius": "CAF",
    "Morocco": "CAF",
    "Mozambique": "CAF",
    "Namibia": "CAF",
    "Niger": "CAF",
    "Nigeria": "CAF",
    "Rwanda": "CAF",
    "São Tomé and Príncipe": "CAF",
    "Senegal": "CAF",
    "Seychelles": "CAF",
    "Sierra Leone": "CAF",
    "Somalia": "CAF",
    "South Africa": "CAF",
    "South Sudan": "CAF",
    "Sudan": "CAF",
    "Tanzania": "CAF",
    "Togo": "CAF",
    "Tunisia": "CAF",
    "Uganda": "CAF",
    "Zambia": "CAF",
    "Zimbabwe": "CAF",

    # AFC
    "Afghanistan": "AFC",
    "Australia": "AFC",
    "Bahrain": "AFC",
    "Bangladesh": "AFC",
    "Bhutan": "AFC",
    "Brunei": "AFC",
    "Cambodia": "AFC",
    "China": "AFC",
    "China PR": "AFC",
    "Guam": "AFC",
    "Hong Kong": "AFC",
    "India": "AFC",
    "Indonesia": "AFC",
    "Iran": "AFC",
    "Iraq": "AFC",
    "Japan": "AFC",
    "Jordan": "AFC",
    "Kuwait": "AFC",
    "Kyrgyzstan": "AFC",
    "Laos": "AFC",
    "Lebanon": "AFC",
    "Macau": "AFC",
    "Malaysia": "AFC",
    "Maldives": "AFC",
    "Mongolia": "AFC",
    "Myanmar": "AFC",
    "Nepal": "AFC",
    "North Korea": "AFC",
    "Oman": "AFC",
    "Pakistan": "AFC",
    "Palestine": "AFC",
    "Philippines": "AFC",
    "Qatar": "AFC",
    "Saudi Arabia": "AFC",
    "Singapore": "AFC",
    "South Korea": "AFC",
    "Korea Republic": "AFC",
    "Sri Lanka": "AFC",
    "Syria": "AFC",
    "Taiwan": "AFC",
    "Tajikistan": "AFC",
    "Thailand": "AFC",
    "Timor-Leste": "AFC",
    "Turkmenistan": "AFC",
    "United Arab Emirates": "AFC",
    "Uzbekistan": "AFC",
    "Vietnam": "AFC",
    "Yemen": "AFC",
    "Yemen DPR": "AFC",

    # OFC
    "American Samoa": "OFC",
    "Cook Islands": "OFC",
    "Fiji": "OFC",
    "New Caledonia": "OFC",
    "New Zealand": "OFC",
    "Papua New Guinea": "OFC",
    "Samoa": "OFC",
    "Solomon Islands": "OFC",
    "Tahiti": "OFC",
    "Tonga": "OFC",
    "Vanuatu": "OFC",

    # Historical / non-FIFA -> Unknown
    "Andalusia": "Unknown",
    "Basque Country": "Unknown",
    "Catalonia": "Unknown",
    "Brittany": "Unknown",
    "Corsica": "Unknown",
    "Galicia": "Unknown",
    "Manchukuo": "Unknown",
    "Northern Cyprus": "Unknown",
    "Silesia": "Unknown",
    "Western Australia": "Unknown",
    "Tibet": "Unknown",
    "Zanzibar": "Unknown",
    "Vietnam Republic": "Unknown",
}

master["federation"] = master["team_name"].map(FEDERATION_MAP).fillna("Unknown")
print("Federations mapped")

unknown = master[master["federation"] == "Unknown"]["team_name"].tolist()
if unknown:
    print(f"\nTeams assigned 'Unknown' federation ({len(unknown)}):")
    for t in unknown:
        print(f"  - {t}")

# --- Step 4: Export ---

master = master[["team_name", "fifa_ranking", "federation"]]
master.to_csv("master_teams.csv", index=False)
print(f"\nExported master_teams.csv ({len(master)} teams)")
