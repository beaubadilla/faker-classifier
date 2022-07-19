import pandas as pd

from subclasses import subclasses
from teams_regions import teams_regions

pd.set_option("display.precision", 2)
pd.set_option("display.max_colwidth", None)
pd.get_option("display.max_colwidth")
pd.set_option("display.max_columns", 999)
pd.set_option("display.max_rows", 100)
def main():
    # df2 = pd.read_csv("C:\\Users\\Alex\\Beau\\ml-practice-proj-faker\\db2.csv", sep="\t")
    # df3 = pd.read_csv("C:\\Users\\Alex\\Beau\\ml-practice-proj-faker\\db3.csv")
    df2 = pd.read_csv("/home/beaujb/Beau/ml-practice-proj-faker/db2.csv", sep="\t")
    df3 = pd.read_csv("/home/beaujb/Beau/ml-practice-proj-faker/db3-next.csv")

    df2['Date_parsed'] = pd.to_datetime(df2['Date'], format="%Y-%m-%d %H:%M:%S")
    df3['Date_parsed'] = pd.to_datetime(df3['date'], format="%Y-%m-%d %H:%M:%S")

    # Find and list dupes
    # pd.concat(g for _, g in df3.groupby("ID") if len(g) > 1)

    df2_drop_dupes = df2.drop_duplicates()
    df3_drop_dupes = df3.drop_duplicates()

    df2_drop_dupes_sorted = df2_drop_dupes.sort_values(by=['Date'])
    df3_drop_dupes_sorted = df3_drop_dupes.sort_values(by=['date'])

    # Get Faker's YoE (unit = tournaments)
    cnt = 0
    tournaments_played = []
    seen = {}
    seen_unique = {}
    t = df2_drop_dupes_sorted.iloc[0].Tournament.split(',')[1]
    for _, row in df2_drop_dupes_sorted.iterrows():
        tournaments_played.append(cnt)
        curr_t = row['Tournament'].split(',')[1]
        if curr_t not in seen:
            seen[curr_t] = 0
        seen[curr_t] += 1
        if curr_t != t:
            # print(f"Tournament {cnt}. Finished with {t} at {seen[t]}")
            if curr_t not in seen_unique:
                seen_unique[curr_t] = 0
            else:
                cnt -= 1
                # print(f'Already seen {curr_t}. -1')
            seen_unique[curr_t] += 1
            t = row['Tournament'].split(',')[1]
            cnt += 1

    df2_drop_dupes_sorted['tournaments_played'] = tournaments_played


    # for db3, add column 'Side' for which side T1/SKT is on. This is to help merge correctly.
    #   on the same note, add 'W/L' if T1/SKT won
    #   'Champion'
    #   'Vs_Champion'
    #   db3-next could have a 'game length' column from the site, but would have to rerun the scraper
    side_col, champion_col, vs_champion_col = [], [], []
    for _, row in df3_drop_dupes_sorted.iterrows():
        if 'Faker' in row['blue_side_roster']:
            side = 'Blue'
            vs_side = 'Red'
        else:
            side = 'Red'
            vs_side = 'Blue'
        fakers_position = row[f"{side.lower()}_side_roster"].split(',').index('Faker')  # in case he was role swapped. don't think he ever did that though
        champion_col.append(row[f"{side.lower()}_side_picks"].split(',')[fakers_position])
        vs_champion_col.append(row[f"{vs_side.lower()}_side_picks"].split(',')[fakers_position])
        side_col.append(side)

    df3_drop_dupes_sorted['Side'] = side_col
    df3_drop_dupes_sorted['Champion'] = champion_col
    df3_drop_dupes_sorted['Vs_Champion'] = vs_champion_col
    # merged = df2_drop_dupes_sorted.merge(df3_drop_dupes_sorted, how='inner')
    # merged = df2_drop_dupes_sorted.merge(df3_drop_dupes_sorted, how='inner', on='Date_parsed')
    merged = df2_drop_dupes_sorted.merge(df3_drop_dupes_sorted, how='inner', on=['Date_parsed', 'Side', 'Champion', 'Vs_Champion'])
    # merged2 = df2_drop_dupes_sorted.merge(df3_drop_dupes_sorted, how='left', on=['Date_parsed'], validate='one_to_one')
    # merged3 = df2_drop_dupes_sorted.merge(df3_drop_dupes_sorted, how='left', right_on="blue_side_team", left_on="Game_Length")
    # merged_no_matches = (df2_drop_dupes_sorted.merge(df3_drop_dupes_sorted, on='Date_parsed', how='outer', indicator=True).query('_merge != "both"').drop('_merge', 1))  # ANTI-JOIN; get records that do not have a match

    merged = pd.read_csv("merged2.csv")
    # Get subclasses (i.e. roles) for each player's champion
    teammate_role_top, teammate_role_jungle, teammate_role_mid, teammate_role_adc, teammate_role_support = [], [], [], [], []
    enemy_role_top, enemy_role_jungle, enemy_role_mid, enemy_role_adc, enemy_role_support = [], [], [], [], []
    for _, row in merged.iterrows():
        blue_side = row['blue_side_roster']
        red_side = row['red_side_roster']

        if 'Faker' in blue_side:
            teammates_champions = row['blue_side_picks']
            opponents_champions = row['red_side_picks']
        elif 'Faker' in red_side:
            teammates_champions = row['red_side_picks']
            opponents_champions = row['blue_side_picks']
        else:
            print(f"Faker not in either team. {row}")

        teammates_champions = teammates_champions.split(',')
        opponents_champions = opponents_champions.split(',')

        teammates_champion_top = teammates_champions[0]
        teammates_champion_jungle = teammates_champions[1]
        teammates_champion_mid = teammates_champions[2]
        teammates_champion_adc = teammates_champions[3]
        teammates_champion_support = teammates_champions[4]
        opponents_champion_top = opponents_champions[0]
        opponents_champion_jungle = opponents_champions[1]
        opponents_champion_mid = opponents_champions[2]
        opponents_champion_adc = opponents_champions[3]
        opponents_champion_support = opponents_champions[4]

        teammate_role_top.append(get_champions_role(teammates_champion_top, 'top'))
        teammate_role_jungle.append(get_champions_role(teammates_champion_jungle, 'jungle'))
        teammate_role_mid.append(get_champions_role(teammates_champion_mid, 'mid'))
        teammate_role_adc.append(get_champions_role(teammates_champion_adc, 'adc'))
        teammate_role_support.append(get_champions_role(teammates_champion_support, 'support'))
        enemy_role_top.append(get_champions_role(opponents_champion_top, 'top'))
        enemy_role_jungle.append(get_champions_role(opponents_champion_jungle, 'jungle'))
        enemy_role_mid.append(get_champions_role(opponents_champion_mid, 'mid'))
        enemy_role_adc.append(get_champions_role(opponents_champion_adc, 'adc'))
        enemy_role_support.append(get_champions_role(opponents_champion_support, 'support'))

    merged['teammate_role_top'] = teammate_role_top
    merged['teammate_role_jungle'] = teammate_role_jungle
    merged['teammate_role_mid'] = teammate_role_mid
    merged['teammate_role_adc'] = teammate_role_adc
    merged['teammate_role_support'] = teammate_role_support
    merged['enemy_role_top'] = enemy_role_top
    merged['enemy_role_jungle'] = enemy_role_jungle
    merged['enemy_role_mid'] = enemy_role_mid
    merged['enemy_role_adc'] = enemy_role_adc
    merged['enemy_role_support'] = enemy_role_support

    merged = pd.read_csv("merged3.csv")
    merged = merged.sort_values(by=["Date_parsed", "Tournament"])
    total, wins, losses = 0, 0, 0
    curr_win_percentage_col, wins_col, losses_col, total_col = [], [], [], []
    t = merged.iloc[0].Tournament
    for _, row in merged.iterrows():
        wins_col.append(wins)
        losses_col.append(losses)
        total_col.append(total)
        if total == 0:
            curr_win_percentage_col.append(0)
        else:
            curr_win_percentage_col.append(round(wins/total, 4))
        curr_t = row.Tournament
        if row['W/L'] == 'Win':
            wins += 1
        else:
            losses += 1
        total += 1
        if curr_t != t:
            wins = 0
            losses = 0
            total = 0
            t = curr_t

    merged['tournament_curr_total_games'] = total_col
    merged['tournament_curr_wins'] = wins_col
    merged['tournament_curr_losses'] = losses_col
    merged['tournament_curr_win_percentage'] = curr_win_percentage_col

    regions = []
    for _, row in merged6.iterrows():
        team = row["Vs_Team"].upper()
        region = teams_regions[team]
        regions.append(region)
    merged['teams_regions'] = regions

    # Split roster. picks, bans
    merged = pd.read_csv("merged8.csv", index_col=0)
    bans = []
    teammate_top_ign, teammate_jungle_ign, teammate_mid_ign, teammate_adc_ign, teammate_support_ign = [], [], [], [], []
    opponent_top_ign, opponent_jungle_ign, opponent_mid_ign, opponent_adc_ign, opponent_support_ign = [], [], [], [], []
    teammate_top_champion, teammate_jungle_champion, teammate_mid_champion, teammate_adc_champion, teammate_support_champion = [], [], [], [], []
    opponent_top_champion, opponent_jungle_champion, opponent_mid_champion, opponent_adc_champion, opponent_support_champion = [], [], [], [], []
    for _, row in merged.iterrows():
        blue_side = row['blue_side_roster']
        red_side = row['red_side_roster']

        if 'Faker' in blue_side:
            teammates_ign = row['blue_side_roster'].split(',')
            opponents_ign = row['red_side_roster'].split(',')
            teammates_champions = row['blue_side_picks'].split(',')
            opponents_champions = row['red_side_picks'].split(',')
        elif 'Faker' in red_side:
            teammates_ign = row['red_side_roster'].split(',')
            opponents_ign = row['blue_side_roster'].split(',')
            teammates_champions = row['red_side_picks'].split(',')
            opponents_champions = row['blue_side_picks'].split(',')
        else:
            print(f"Faker not in either team. {row}")
        teammate_top_champion.append(teammates_champions[0])
        teammate_jungle_champion.append(teammates_champions[1])
        teammate_mid_champion.append(teammates_champions[2])
        teammate_adc_champion.append(teammates_champions[3])
        teammate_support_champion.append(teammates_champions[4])
        opponent_top_champion.append(opponents_champions[0])
        opponent_jungle_champion.append(opponents_champions[1])
        opponent_mid_champion.append(opponents_champions[2])
        opponent_adc_champion.append(opponents_champions[3])
        opponent_support_champion.append(opponents_champions[4])

        teammate_top_ign.append(teammates_ign[0])
        teammate_jungle_ign.append(teammates_ign[1])
        # teammate_mid_ign.append(teammates_ign[2])
        teammate_adc_ign.append(teammates_ign[3])
        teammate_support_ign.append(teammates_ign[4])
        opponent_top_ign.append(opponents_ign[0])
        opponent_jungle_ign.append(opponents_ign[1])
        opponent_mid_ign.append(opponents_ign[2])
        opponent_adc_ign.append(opponents_ign[3])
        opponent_support_ign.append(opponents_ign[4])
        ban = ','.join(sorted((row['red_side_bans'] + ',' + row['blue_side_bans']).split(',')))
        bans.append(ban)

    merged['bans'] = bans
    merged['teammate_top_champion'] = teammate_top_champion
    merged['teammate_jungle_champion'] = teammate_jungle_champion
    merged['teammate_mid_champion'] = teammate_mid_champion
    merged['teammate_adc_champion'] = teammate_adc_champion
    merged['teammate_support_champion'] = teammate_support_champion
    merged['opponent_top_champion'] = opponent_top_champion
    merged['opponent_jungle_champion'] = opponent_jungle_champion
    merged['opponent_mid_champion'] = opponent_mid_champion
    merged['opponent_adc_champion'] = opponent_adc_champion
    merged['opponent_support_champion'] = opponent_support_champion

    merged['teammate_top_ign'] = teammate_top_ign
    merged['teammate_jungle_ign'] = teammate_jungle_ign
    # merged['teammate_mid_ign'] = teammate_mid_ign
    merged['teammate_adc_ign'] = teammate_adc_ign
    merged['teammate_support_ign'] = teammate_support_ign
    merged['opponent_top_ign'] = opponent_top_ign
    merged['opponent_jungle_ign'] = opponent_jungle_ign
    merged['opponent_mid_ign'] = opponent_mid_ign
    merged['opponent_adc_ign'] = opponent_adc_ign
    merged['opponent_support_ign'] = opponent_support_ign

    merged.to_csv("merged9.csv", index=False)

def get_champions_role(champion, lane):
    # cls, subcls = None, None

    if champion == 'Nunu': champion = 'Nunu & Willump'
    classes = subclasses[champion].split()
    # num_of_classes = len(classes) / 2
    if champion == 'Varus':
        if lane == 'adc':
            subcls = classes[1]
        else:
            subcls = classes[3]
    else:
        subcls = classes[1]

    return subcls

if __name__ == '__main__':
    main()
