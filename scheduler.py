import pandas as pd
import random

HISTORY_FILENAME = "pair_history.csv"
LIMITATIONS_FILENAME = "limitations.csv"
MAX_MEETINGS = 5

class ValidationError(Exception):
    pass

def validate_history(history_df):
    if (not history_df.equals(history_df.T)):
        raise ValidationError("error in pair history, make sure row and column entries match")
    else:
        return True

def match_slots(series_one, series_two):
    available_slots = series_one[series_one == series_two]
    if len(available_slots) == 0:
        return "", False
    return available_slots.sample().index, True

def occupied_slots(availability_df, fellow):
    return len(availability_df[fellow][(availability_df[fellow] == "True") | (availability_df[fellow] == "False")])

def assign_coaches(history_df, availability_df):
    coach_columns = availability_df.columns.str.startswith("[COACH]")
    for coach, _ in availability_df.loc[:, coach_columns].items():
        available_fellows = history_df[coach].loc[(history_df[coach] == "False") & ~coach_columns].index
        for fellow in available_fellows:
            # if occupied_slots(availability_df, fellow) < MAX_MEETINGS:
                slot, found = match_slots(availability_df[coach], availability_df[fellow])
                if found:
                    availability_df.loc[slot, coach] = fellow
                    availability_df.loc[slot, fellow] = coach
                    history_df.loc[fellow, coach] = "True"
                    history_df.loc[coach, fellow] = "True"

    return history_df, availability_df

def load_history(filename):
    history = pd.read_csv(filename, index_col=0,true_values=["X","x"]).fillna("False").replace(to_replace=True, value="True")
    validate_history(history)
    return history

def load_availability(filename):
    return pd.read_csv(filename, index_col=0,false_values=["X","x"]).fillna("True").replace(to_replace=False, value="False")

def main():
    pd.options.mode.copy_on_write = True
    history = load_history(HISTORY_FILENAME)
    availability = load_availability(LIMITATIONS_FILENAME)

    # print(history)
    # print(availability)
    print("---")

    assign_coaches(history, availability)

    # print(availability)


if __name__=="__main__":
    main()