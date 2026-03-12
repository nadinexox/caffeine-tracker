from my_module.functions import calculate_decay, minutes_until_threshold

def test_calculate_decay():
    """
    Test the caffeine decay calculation for accuracy.
    """
    # Test 1: After exactly one half-life (5 hours), 200mg should be 100mg
    assert calculate_decay(200, 5) == 100.0
    # Test 2: At 0 hours, the amount should still be the initial amount
    assert calculate_decay(200, 0) == 200.0

def test_minutes_until_threshold():
    """
    Test the prediction logic for minutes remaining until a caffeine crash.
    """
    #Ttest 3: If we are already below the threshold, it should return 0
    assert minutes_until_threshold(40, 50) == 0
    # Test 4: Check if the prediction logic is correct
    # Standard decay (100mg to 50mg is exactly 1 half-life = 300 minutes)
    assert minutes_until_threshold(100, 50) == 300.0