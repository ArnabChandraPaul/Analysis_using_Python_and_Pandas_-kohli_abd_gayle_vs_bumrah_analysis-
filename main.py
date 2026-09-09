import pandas as pd
import json
import os
import glob

# 1. Process all Json files
folder_path = 'ipl_male_json'

if not os.path.exists(folder_path):
    print(f"Error: Folder '{folder_path}' not found")
    exit()

json_files = glob.glob(f'{folder_path}/*.json')
print(f'Processing {len(json_files)} IPL match JSON files...')

ball_records = []

for file in json_files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for innings in data.get('innings', []):
            for over in innings.get('overs', []):
                for delivery in over.get('deliveries', []):
                    batter = delivery.get('batter')
                    bowler = delivery.get('bowler')
                    runs_batter = delivery.get('runs', {}).get('batter', 0)

                    wicket_type = None
                    if 'wickets' in delivery:
                        wicket_type = delivery['wickets'][0].get('kind')

                    ball_records.append({
                        'batter': batter,
                        'bowler': bowler,
                        'runs': runs_batter,
                        'wicket': wicket_type,})
    except Exception:
        pass

df = pd.DataFrame(ball_records)

# 2. Match analysis function
def analysze_matchup(batter_name, bowler_name):
    data = df[(df['batter'] == batter_name) & (df['bowler'] == bowler_name)]
    total_balls = len(data)

    if total_balls == 0:
        print("No record")
        return

    total_runs = data['runs'].sum()
    strike_rate = (total_runs/total_balls)*100
    dismissals = data['wicket'].dropna().count()
    fours = len(data[data['runs'] == 4])
    sixes = len(data[data['runs'] == 6])
    dots = len(data[data['runs'] == 0])

    print("\n" + "="*45)
    print(f'IPL Match Report: {batter_name} vs {bowler_name}')
    print("="*45)
    print(f"Balls Faced  : {total_balls}")
    print(f"Total Runs   : {total_runs}")
    print(f"Strike rate  : {strike_rate:.2f}")
    print(f"Dismissals   : {dismissals}")
    print(f"Dots         : {dots}")
    print(f"Fours (4s)   : {fours} | Sixes (6s): {sixes}")
    print("="*45)


# 3. Reselt
analysze_matchup("V Kohli", "JJ Bumrah")
analysze_matchup("AB de Villiers", "JJ Bumrah")
analysze_matchup("CH Gayle", "JJ Bumrah")
 