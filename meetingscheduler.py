import random 
from itertools import combinations 
import pandas as pd
import random

# Function to read matrix from a CSV file
def read_matrix(file_path):
    # Read the matrix from a CSV file
    df = pd.read_csv(file_path, index_col=0)
    return df

matrix = read_matrix("pairing_matrix.csv")
participants = [f"Person {i}" for i in range(1, 27)] 

time_slots = [ "9:00 - 9:30", "9:30 - 10:00", "10:00 - 10:30", "10:30 - 11:00", "11:00 - 11:30", "11:30 - 12:00", "4:00 - 4:30", "4:30 - 5:00"] 
# Initialize a list to keep track of pairs
pair_history = set()
match_count = {participant: 0 for participant in participants}
# Function to create pairs 
def create_pairs(participants): 
    random.shuffle(participants) 
    pairs = [] 
    for i in range(0, len(participants), 2): 
        if i + 1 < len(participants): 
            pairs.append((participants[i], participants[i + 1])) 
    return pairs 
        # Generate pairings for each time slot 
schedule = {} 
for slot in time_slots: 
    while True: 
        pairs = create_pairs(participants) 
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

matrix.to_csv('pairing_matrix.csv')
# TODO read csv file and export the new matches