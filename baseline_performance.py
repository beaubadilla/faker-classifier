from re import sub
from sys import exit
from platform import system

from pandas import read_csv
from pandas.core import frame


def main():
    # Get file path
    if system() == "Windows":
        filepath = "C:\\Users\\Beau\\Desktop\\ML\\faker\\merged9.csv"
    # elif system() == "Linux":
    # filepath = ""
    else:
        print(f"Unfamiliar OS. Cannot set file path to csv file.")
        exit(1)

    # Load csv
    print(f'Loading "{filepath}"')
    dataframe = read_csv(filepath)
    print(dataframe.head())

    cols = dataframe.columns

    # Select random subset of 100
    size_subset = 20
    dataframe_subset = dataframe.sample(n=size_subset, random_state=2)

    # Make predictions
    correct = 0
    predictions = []
    for game in dataframe_subset.itertuples():
        # print game details
        print(game_details(game))

        # prompt for prediction
        prediction = ""
        while prediction not in ["win", "loss"]:
            prediction = input(f"Win or loss? ").lower()
            if prediction not in ["win", "loss"]:
                print(f"Invalid response. Try again.")

        # record prediction
        predictions.append(prediction)

    # calculate accuracy
    accuracy_breakdown(dataframe_subset, predictions)
    # accuracy_breakdown(
    #     dataframe_subset, predictions, fp_examples=True, fn_examples=True
    # )


def game_details(game: frame) -> str:
    # Current Record at Tournament: win-loss
    # (blue)player1, player2, player3, player4, player5
    # (red)player1, player2, *Faker*, player4, player5
    # (blue)Team: win-loss (region)
    # (red)Team: win-loss (region)

    # Blue - champ1...
    # Red - champ1...
    # Bans
    # Bans
    # Spells

    # prep variables for readability
    win = game.tournament_curr_wins
    loss = game.tournament_curr_losses
    details = (
        f"-----------------------------------------------\n"
        f"Current record at {game.Tournament}: {win} wins/{loss} losses\n"
        f"{game.blue_side_roster}\n"
        f"{game.red_side_roster}\n"
        f"{game.blue_side_team} ({game.teams_region})\n"
        f"{game.red_side_team} ({game.teams_region})\n"
        "\n"
        f"PICKS:{game.blue_side_picks}\n"
        f"PICKS:{game.red_side_picks}\n"
        f"BANS:{game.blue_side_bans}\n"
        f"BANS:{game.red_side_bans}\n"
        f"{game.Spells}\n"
    )
    details = details.replace("Faker", "*Faker*")

    # Some IGNs have the player's real name because of duplicate IGNs
    unnecessary = r"\s\([a-zA-Z\s-]*\)"
    details = sub(unnecessary, "", details)

    return details


def accuracy_breakdown(
    dataframe,
    predictions,
    tp_examples: bool = False,
    tn_examples: bool = False,
    fp_examples: bool = False,
    fn_examples: bool = False,
):
    # Type 1 error:
    # Type 2 error:
    # True positive: correct prediction, prediction is win
    # True negative: correct prediction, prediction is loss
    # False positive: incorrect prediction, prediction is win
    # False negative: incorrect prediction, prediction is loss

    # print accuracy
    # print precision - future
    # print type 1 error accuracy (fp)
    # print type 2 error accuracy (fn)
    # if correct
    correct = 0
    tp_indices, tn_indices, fp_indices, fn_indices = [], [], [], []
    for i in range(len(dataframe)):
        frame = dataframe.iloc[i]

        prediction = predictions[i]
        target = frame["W/L"].lower()
        index = frame.name

        if prediction == target and prediction == "win":
            tp_indices.append(index)
            correct += 1
        elif prediction == target and prediction == "loss":
            tn_indices.append(index)
            correct += 1
        elif prediction != target and prediction == "win":
            fp_indices.append(index)
        elif prediction != target and prediction == "loss":
            fn_indices.append(index)

    m = len(dataframe)
    num_errors = m - correct
    overall_accuracy = correct / m
    type1_accuracy = len(fp_indices) / num_errors
    type2_accuracy = len(fn_indices) / num_errors
    print(f"Accuracy={overall_accuracy:.2f}")
    print(f"Type 1={type1_accuracy * 100:.2f}% of errors")
    print(f"Type 2={type2_accuracy * 100:.2f}% of errors")

    if tp_examples:
        print(f"Displaying True Positive Examples\n")
        for i in tp_indices:
            print(dataframe.loc[i])
    elif tn_examples:
        print(f"Displaying True Negative Examples\n")
        for i in tn_indices:
            print(dataframe.loc[i])
    elif fp_examples:
        print(f"Displaying False Positive Examples\n")
        for i in fp_indices:
            print(dataframe.loc[i])
    elif fn_examples:
        print(f"Displaying False Negative Examples\n")
        for i in fn_indices:
            print(dataframe.loc[i])


if __name__ == "__main__":
    main()

# temp
# details = None
# for game in dataframe.itertuples():
#     details = game_details(game)
#     print(details)
#     break
