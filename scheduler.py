import pandas as pd

HISTORY_FILENAME = "pair_history.csv"
LIMITATIONS_FILENAME = "limitations.csv"
MAX_MEETINGS = 5
OPTIMIZE_RUNS = 10

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
    total_slots = len(availability_df[fellow])
    return total_slots - len(availability_df[fellow][(availability_df[fellow] == "True") | (availability_df[fellow] == "False")])

def assign_coach_or_fellow(history_df, availability_df, max_meetings, coach_columns, coach_or_fellow):
    available_fellows = history_df[coach_or_fellow].loc[(history_df[coach_or_fellow] == "False") & ~coach_columns].index
    for fellow in available_fellows:
        if occupied_slots(availability_df, fellow) < max_meetings:
            slot, found = match_slots(availability_df[coach_or_fellow], availability_df[fellow])
            if found:
                availability_df.loc[slot, coach_or_fellow] = fellow
                availability_df.loc[slot, fellow] = coach_or_fellow
                history_df.loc[fellow, coach_or_fellow] = "True"
                history_df.loc[coach_or_fellow, fellow] = "True"

    return history_df, availability_df

def assign_coaches(history_df, availability_df, max_meetings):
    coach_columns = availability_df.columns.str.startswith("[COACH]")
    for coach, _ in availability_df.loc[:, coach_columns].items():
        assign_coach_or_fellow(history_df, availability_df, max_meetings, coach_columns, coach)

def assign_fellows(history_df, availability_df, max_meetings):
    coach_columns = availability_df.columns.str.startswith("[COACH]")
    for fellow, _ in availability_df.loc[:, ~coach_columns].items():
        assign_coach_or_fellow(history_df, availability_df, max_meetings, coach_columns, fellow)

    return history_df, availability_df

def optimize_schedule(history_df, availability_df, max_meetings, optimize_runs):
    optimal_history = history_df.copy()
    optimal_availability = availability_df.copy()

    optimal_slots = (optimal_availability.values == "True").sum()
    for i in range(optimize_runs):
        ongoing_availability = availability_df.copy()
        ongoing_history = history_df.copy()
        assign_coaches(ongoing_history, ongoing_availability, max_meetings)
        assign_fellows(ongoing_history, ongoing_availability, max_meetings)
        open_slots = (ongoing_availability.values == "True").sum()
        if open_slots < optimal_slots:
            print(i)
            optimal_slots = open_slots
            optimal_availability = ongoing_availability.copy()
            optimal_history = ongoing_history.copy()

    return optimal_history, optimal_availability

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
    # print("---")

    history, availability = optimize_schedule(history, availability, MAX_MEETINGS, OPTIMIZE_RUNS)

    # print(availability)


if __name__=="__main__":
    main()