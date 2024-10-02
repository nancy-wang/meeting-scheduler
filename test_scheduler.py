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
    assert scheduler.occupied_slots(availability,"[COACH]Windu") == 6
    
    history = scheduler.load_history('test/good_history.csv')
    scheduler.assign_coaches(history, availability)

    assert scheduler.occupied_slots(availability,"[COACH]Windu") == 3

def test_assign_coaches():
    history = scheduler.load_history('test/good_history.csv')
    availability = scheduler.load_availability('test/limitations.csv')

    scheduler.assign_coaches(history, availability)

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

    scheduler.assign_coaches(history, availability)
    
    assert (availability['[COACH]Yoda'] == "Luke").any()
    assert (availability['[COACH]Maul'] == "Luke").any()
    assert (availability['[COACH]Obi'] == "Luke").any()
    assert (availability['[COACH]Anakin'] == "Luke").any()
    assert (availability['[COACH]Windu'] == "Luke").any()

    assert (availability['Luke'] == "[COACH]Yoda").any()
    assert (availability['Luke'] == "[COACH]Maul").any()
    assert (availability['Luke'] == "[COACH]Obi").any()
    assert (availability['Luke'] == "[COACH]Anakin").any()
    assert (availability['Luke'] == "[COACH]Windu").any()