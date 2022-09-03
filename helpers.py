from pandas import Series

from champion_dmg_profile import champion_dmg_profile


def get_damage_profile_composition(match: Series):
    """
    Must have a Series object as the parameter if we want to use pandas.DataFrame.apply()
    """
    # get blue side picks
    blue_side_picks = match["blue_side_picks"].split(",")
    # get red side picks
    red_side_picks = match["red_side_picks"].split(",")

    # get blue picks info with comprehension
    blue_team_info = {champ: champion_dmg_profile[champ] for champ in blue_side_picks}
    # get red picks info with comprehension
    red_team_info = {champ: champion_dmg_profile[champ] for champ in red_side_picks}

    # calculate weights
    # sum DPM
    sum_blue_dpm = sum((info["DPM"] for info in blue_team_info.values()))
    for info in blue_team_info.values():
        curr_champ_dpm = info["DPM"]
        info["weight"] = curr_champ_dpm / sum_blue_dpm
    sum_red_dpm = sum((info["DPM"] for info in red_team_info.values()))
    for info in red_team_info.values():
        curr_champ_dpm = info["DPM"]
        info["weight"] = curr_champ_dpm / sum_red_dpm

    blue_physical_damage_perc = sum(
        info["weight"] * info["physical_damage"] for info in blue_team_info.values()
    )
    blue_magic_damage_perc = sum(
        info["weight"] * info["magic_damage"] for info in blue_team_info.values()
    )
    blue_true_damage_perc = sum(
        info["weight"] * info["true_damage"] for info in blue_team_info.values()
    )
    red_physical_damage_perc = sum(
        info["weight"] * info["physical_damage"] for info in red_team_info.values()
    )
    red_magic_damage_perc = sum(
        info["weight"] * info["magic_damage"] for info in red_team_info.values()
    )
    red_true_damage_perc = sum(
        info["weight"] * info["true_damage"] for info in red_team_info.values()
    )

    return (
        blue_physical_damage_perc,
        blue_magic_damage_perc,
        blue_true_damage_perc,
        red_physical_damage_perc,
        red_magic_damage_perc,
        red_true_damage_perc,
    )
