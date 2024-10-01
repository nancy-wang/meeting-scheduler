import random 
import pandas as pd

class Fellow:
    def __init__(self, name, time_slots, already_met_fellows, already_met_coaches):
        self.name = name
        self.time_slots = time_slots
        self.already_met_fellows = already_met_fellows
        self.already_met_coaches = already_met_coaches
    
    def __str__(self):
        return f'{self.name} {self.time_slots} Fellows met with: \n \t {self.already_met_fellows} Coaches met with: \n \t {self.already_met_coaches}'

    def __repr__(self):
        return f'{self.name} {self.time_slots} Fellows met with: \n \t {self.already_met_fellows} Coaches met with: \n \t {self.already_met_coaches}'

# Function to read matrix from a CSV file
def read_matrix(file_path):
    # Read the matrix from a CSV file
    df = pd.read_csv(file_path, index_col=0)
    return df

matrix = read_matrix("~/Downloads/pair_history.csv")

matrix = matrix.map(lambda elem: "x", na_action="ignore")

participants = matrix.index.to_series()
coach_names = participants[participants.str.startswith("[COACH]", na=False)]
fellow_names = participants[~participants.str.startswith("[COACH]", na=False)]

# for each of the fellows, define them as the name of the person which is fellow[i], time_slots is empty, already_met can be filled thru the spreadsheet
fellows = []
for fellow in fellow_names:
    already_met_people_df = matrix.loc[(matrix[fellow]=="x")]
    already_met_people = already_met_people_df.iloc[:,0]
    already_met_coaches = already_met_people[already_met_people.index.str.startswith("[COACH]", na=False)]
    already_met_fellows = already_met_people[~already_met_people.index.str.startswith("[COACH]", na=False)]
    new_fellow = Fellow(fellow, (), already_met_fellows, already_met_coaches)
    fellows.append(new_fellow)

'''
time_slots = [ "9:00 - 9:30", "9:30 - 10:00", "10:00 - 10:30", "10:30 - 11:00", "11:00 - 11:30", "11:30 - 12:00", "4:00 - 4:30", "4:30 - 5:00"] 
# Initialize a list to keep track of pairs
pair_history = set()
match_count = {participant: 0 for participant in participants}
# Function to create pairs 
def create_pairs(participants, matrix):
    random.shuffle(participants) 
    pairs = [] 
    for i in range(0, len(participants), 2): 
        if i + 1 < len(participants): 
                pairs.append((participants.iloc[i], participants.iloc[i + 1])) 
                # track number of conflicts and see which has least amount, return this sequence at the end
    return pairs 

# Generate pairings for each time slot 
schedule = {} 
for slot in time_slots: 
    while True:
        pairs = create_pairs(participants, matrix) 
        print(pairs)
        # Check if any pairs have already met 
        if not any(pair in pair_history or (pair[1], pair[0]) in pair_history for pair in pairs):
            if all(match_count[p1] < 5 and match_count[p2] < 5 for p1, p2 in pairs):
                schedule[slot] = pairs 
                for p1, p2 in pairs: 
                    pair_history.add((p1, p2)) 
                    match_count[p1] += 1
                    match_count[p2] += 1
                    matrix.at[p1, p2] = slot
                    matrix.at[p2, p1] = slot
                break
            break


# Print the schedule 
for time_slot, pairs in schedule.items(): 
    for p1, p2 in pairs: 
        print(f"{time_slot}: {p1} meets {p2}") 

matrix.to_csv('~/Downloads/pair_history.csv')
'''
# TODO read csv file and export the new matches