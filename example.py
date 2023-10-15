import pandas as pd
import os
import json


def load_data(json_dir):
    """Loads all JSON files in the given directory into a single DataFrame."""
    file_paths = [os.path.join(json_dir, file) for file in os.listdir(json_dir) if file.endswith(".json")]
    dataframes = []
    for file_path in file_paths:
        with open(file_path, "r") as f:
            json_data = json.loads(f.read())
        slots_dataframe = pd.DataFrame(json_data["response"]["slots"]["slots"])
        dataframes.append(slots_dataframe)
    df = pd.concat(dataframes, ignore_index=True)
    df = df.drop(columns=["bonushunt_slot_position", "bonushunt_slot_opened", "bonushunt_slot_next", "bonushunt_slot_currency"])
    df = df.rename(columns={"bonushunt_slot_position": "position", "bonushunt_slot_name": "slot_name", "bonushunt_slot_provider": "provider", "bonushunt_slot_bet": "bet", "bonushunt_slot_mp": "multiplier", "bonushunt_slot_win": "win", "bonushunt_casino_name": "casino"})
    return df


def count_mult(df, data):
    """Counts the number of bonuses that are greater than or equal to the given data and prints the results."""
    count = (df["multiplier"] > data).count()
    sum = (df["multiplier"] > data).sum()
    rate = count / sum
    print(f"Roshtein made {data}x or more {sum} times of {count} bonuses.")
    print(f"The rate of him hitting {data}x is once every {int(rate)} bonus")


if __name__ == "__main__":
    json_dir = "Datafiles/"
    df = load_data(json_dir)
    count_mult(df, 100)
