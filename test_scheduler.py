import scheduler
import pandas as pd
import pytest

def test_validate_history_bad():
    with pytest.raises(scheduler.ValidationError):
        bad_history = scheduler.load_history('test/bad_history.csv')
        scheduler.validate_history(bad_history)

def test_validate_history_good():
    good_history = scheduler.load_history('test/good_history.csv')
    assert scheduler.validate_history(good_history)

def test_occupied_slots():
    availability = scheduler.load_availability('test/limitations.csv')
    assert scheduler.occupied_slots(availability,"[COACH]Windu") == 0
    
    history = scheduler.load_history('test/good_history.csv')
    scheduler.assign_coaches(history, availability, 5)

    assert scheduler.occupied_slots(availability,"[COACH]Windu") == 3

def test_assign_coaches():
    history = scheduler.load_history('test/good_history.csv')
    availability = scheduler.load_availability('test/limitations.csv')

    scheduler.assign_coaches(history, availability, 5)

    assert (availability['[COACH]Yoda'] == "Maul").any()
    assert (availability['Maul'] == "[COACH]Yoda").any()
    assert not (availability['[COACH]Yoda'] == "Obi").any()
    assert not (availability['[COACH]Yoda'] == "Luke").any()
    assert not (availability['[COACH]Yoda'] == "Anakin").any()

    assert (availability['[COACH]Windu'] == "Obi").any()
    assert (availability['Obi'] == "[COACH]Windu").any()
    assert (availability['[COACH]Windu'] == "Luke").any()
    assert (availability['Luke'] == "[COACH]Windu").any()
    assert (availability['[COACH]Windu'] == "Maul").any()
    assert (availability['Maul'] == "[COACH]Windu").any()
    assert not (availability['[COACH]Windu'] == "Anakin").any()

    assert history['[COACH]Yoda']['Maul'] == "True"
    assert history['Maul']['[COACH]Yoda'] == "True"

    assert (history['[COACH]Windu']["Obi"]) == "True"
    assert (history['Obi']["[COACH]Windu"]) == "True"
    assert (history['[COACH]Windu']["Luke"]) == "True"
    assert (history['Luke']["[COACH]Windu"]) == "True"
    assert (history['[COACH]Windu']["Maul"]) == "True"
    assert (history['Maul']["[COACH]Windu"]) == "True"

def test_assign_coaches_coach_galore():
    history = scheduler.load_history('test/coach_ahoy_history.csv')
    availability = scheduler.load_availability('test/coach_ahoy_limits.csv')

    scheduler.assign_coaches(history, availability, 6)
    
    assert (availability['[COACH]Yoda'] == "Luke").any()
    assert (availability['[COACH]Maul'] == "Luke").any()
    assert (availability['[COACH]Obi'] == "Luke").any()
    assert (availability['[COACH]Anakin'] == "Luke").any()
    assert (availability['[COACH]Windu'] == "Luke").any()
    assert (availability['[COACH]Palp'] == "Luke").any()

    assert (availability['Luke'] == "[COACH]Yoda").any()
    assert (availability['Luke'] == "[COACH]Maul").any()
    assert (availability['Luke'] == "[COACH]Obi").any()
    assert (availability['Luke'] == "[COACH]Anakin").any()
    assert (availability['Luke'] == "[COACH]Windu").any()
    assert (availability['Luke'] == "[COACH]Palp").any()

def test_assign_coaches_coach_galore_maxed():
    history = scheduler.load_history('test/coach_ahoy_history.csv')
    availability = scheduler.load_availability('test/coach_ahoy_limits.csv')

    scheduler.assign_coaches(history, availability, 5)

    assert (availability['[COACH]Yoda'] == "Luke").any()
    assert (availability['[COACH]Maul'] == "Luke").any()
    assert (availability['[COACH]Obi'] == "Luke").any()
    assert (availability['[COACH]Anakin'] == "Luke").any()
    assert (availability['[COACH]Windu'] == "Luke").any()
    assert not (availability['[COACH]Palp'] == "Luke").any()

    assert (availability['Luke'] == "[COACH]Yoda").any()
    assert (availability['Luke'] == "[COACH]Maul").any()
    assert (availability['Luke'] == "[COACH]Obi").any()
    assert (availability['Luke'] == "[COACH]Anakin").any()
    assert (availability['Luke'] == "[COACH]Windu").any()
    assert not (availability['Luke'] == "[COACH]Palp").any()

def test_assign_fellows():
    history = scheduler.load_history('test/good_history.csv')
    availability = scheduler.load_availability('test/limitations.csv')

    scheduler.assign_fellows(history, availability, 5)

    assert (availability['Anakin'] == "Obi").any()
    assert (availability['Anakin'] == "Maul").any()
    assert (availability['Luke'] == "Maul").any()
    assert (availability['Obi'] == "Anakin").any()
    assert (availability['Maul'] == "Luke").any()
    assert (availability['Maul'] == "Anakin").any()

    assert (history['Anakin']['Obi'])
    assert (history['Anakin']['Maul'])
    assert (history['Luke']['Maul'])
    assert (history['Obi']['Anakin'])
    assert (history['Maul']['Luke'])
    assert (history['Maul']['Anakin'])

def test_assign_fellows_fresh():
    history = scheduler.load_history('test/fresh_history.csv')
    availability = scheduler.load_availability('test/fresh_limits.csv')

    scheduler.assign_fellows(history, availability, 5)

    assert (availability['Anakin'] == "Obi").any()
    assert (availability['Anakin'] == "Maul").any()
    assert (availability['Anakin'] == "Luke").any()
    assert (availability['Anakin'] == "Palp").any()
    assert (availability['Luke'] == "Anakin").any()
    assert (availability['Luke'] == "Obi").any()
    assert (availability['Luke'] == "Maul").any()
    assert (availability['Luke'] == "Palp").any()
    assert (availability['Obi'] == "Anakin").any()
    assert (availability['Obi'] == "Anakin").any()
    assert (availability['Obi'] == "Luke").any()
    assert (availability['Obi'] == "Maul").any()
    assert (availability['Obi'] == "Palp").any()
    assert (availability['Maul'] == "Luke").any()
    assert (availability['Maul'] == "Anakin").any()
    assert (availability['Maul'] == "Obi").any()
    assert (availability['Maul'] == "Palp").any()

    assert (history['Anakin']['Luke'])
    assert (history['Anakin']['Obi'])
    assert (history['Anakin']['Maul'])
    assert (history['Anakin']['Palp'])
    assert (history['Luke']['Anakin'])
    assert (history['Luke']['Obi'])
    assert (history['Luke']['Maul'])
    assert (history['Luke']['Palp'])
    assert (history['Obi']['Anakin'])
    assert (history['Obi']['Luke'])
    assert (history['Obi']['Maul'])
    assert (history['Obi']['Palp'])
    assert (history['Maul']['Anakin'])
    assert (history['Maul']['Luke'])
    assert (history['Maul']['Obi'])
    assert (history['Maul']['Palp'])
    assert (history['Maul']['Anakin'])

def test_assign_coaches_and_fellows_fresh():
    history = scheduler.load_history('test/fresh_history.csv')
    availability = scheduler.load_availability('test/fresh_limits.csv')

    scheduler.assign_coaches(history, availability, 5)
    scheduler.assign_fellows(history, availability, 5)

    # coaches take priority
    assert (availability['[COACH]Yoda'] == "Maul").any()
    assert (availability['Maul'] == "[COACH]Yoda").any()
    assert (availability['[COACH]Yoda'] == "Anakin").any()
    assert (availability['Anakin'] == "[COACH]Yoda").any()
    assert (availability['[COACH]Yoda'] == "Obi").any()
    assert (availability['Obi'] == "[COACH]Yoda").any()
    assert (availability['[COACH]Yoda'] == "Palp").any()
    assert (availability['Palp'] == "[COACH]Yoda").any()
    assert (availability['[COACH]Yoda'] == "Luke").any()
    assert (availability['Luke'] == "[COACH]Yoda").any()

    assert (availability['[COACH]Windu'] == "Maul").any()
    assert (availability['Maul'] == "[COACH]Windu").any()
    assert (availability['[COACH]Windu'] == "Anakin").any()
    assert (availability['Anakin'] == "[COACH]Windu").any()
    assert (availability['[COACH]Windu'] == "Obi").any()
    assert (availability['Obi'] == "[COACH]Windu").any()
    assert (availability['[COACH]Windu'] == "Palp").any()
    assert (availability['Palp'] == "[COACH]Windu").any()
    assert (availability['[COACH]Windu'] == "Luke").any()
    assert (availability['Luke'] == "[COACH]Windu").any()

    # each fellow meets with at least 2 other fellows
    assert availability['Anakin'].isin(["Obi","Maul","Luke","Palp"]).sum() >= 2
    assert availability['Obi'].isin(["Anakin","Maul","Luke","Palp"]).sum() >= 2
    assert availability['Maul'].isin(["Obi","Anakin","Luke","Palp"]).sum() >= 2
    assert availability['Luke'].isin(["Obi","Maul","Anakin","Palp"]).sum() >= 2
    assert availability['Palp'].isin(["Obi","Maul","Luke","Anakin"]).sum() >= 2

def test_optimize_schedule():
    history = scheduler.load_history('test/fresh_history.csv')
    availability = scheduler.load_availability('test/fresh_limits.csv')

    history, availability = scheduler.optimize_schedule(history, availability, 5, 10)

    # coaches take priority
    assert (availability['[COACH]Yoda'] == "Maul").any()
    assert (availability['Maul'] == "[COACH]Yoda").any()
    assert (availability['[COACH]Yoda'] == "Anakin").any()
    assert (availability['Anakin'] == "[COACH]Yoda").any()
    assert (availability['[COACH]Yoda'] == "Obi").any()
    assert (availability['Obi'] == "[COACH]Yoda").any()
    assert (availability['[COACH]Yoda'] == "Palp").any()
    assert (availability['Palp'] == "[COACH]Yoda").any()
    assert (availability['[COACH]Yoda'] == "Luke").any()
    assert (availability['Luke'] == "[COACH]Yoda").any()

    assert (availability['[COACH]Windu'] == "Maul").any()
    assert (availability['Maul'] == "[COACH]Windu").any()
    assert (availability['[COACH]Windu'] == "Anakin").any()
    assert (availability['Anakin'] == "[COACH]Windu").any()
    assert (availability['[COACH]Windu'] == "Obi").any()
    assert (availability['Obi'] == "[COACH]Windu").any()
    assert (availability['[COACH]Windu'] == "Palp").any()
    assert (availability['Palp'] == "[COACH]Windu").any()
    assert (availability['[COACH]Windu'] == "Luke").any()
    assert (availability['Luke'] == "[COACH]Windu").any()

    # each fellow meets with at least 2 other fellows
    assert availability['Anakin'].isin(["Obi","Maul","Luke","Palp"]).sum() >= 2
    assert availability['Obi'].isin(["Anakin","Maul","Luke","Palp"]).sum() >= 2
    assert availability['Maul'].isin(["Obi","Anakin","Luke","Palp"]).sum() >= 2
    assert availability['Luke'].isin(["Obi","Maul","Anakin","Palp"]).sum() >= 2
    assert availability['Palp'].isin(["Obi","Maul","Luke","Anakin"]).sum() >= 2
