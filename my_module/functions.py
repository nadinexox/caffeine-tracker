import math

def hours_passed(timestamp, current_time):
    """
    Amt of time passed between log entry and now
    Parameters
    ----------
    timestamp: The time the drink was logged
    current_time: The current time

    Returns
    -------
    float: The difference between the two times in hours.
    """
    diff = current_time - timestamp
    return diff.total_seconds() / 3600


def calculate_decay(initial_mg, hours_passed, half_life=5.0):
    """
    Calculating the remaining caffeine in body using exponential decay.
    
    Parameters:
    -------
    initial_mg (float): Starting amy of caffeine.
    hours_passed (float): Amt of hours since consumption.
    half_life (float): The half-life of the caffeine (usually 5 hrs for most people).
    """
    # If the time given is in the future, return initial amount
    if hours_passed < 0:
        return initial_mg
        
    # Exponential decay formula: N(t) = N0 * (0.5 ^ (t/h)) 
    remaining = initial_mg * (0.5 ** (hours_passed / half_life))
    return round(remaining, 2)


def get_historical_mg(log_time, full_df):
    """
    Parameters
    ----------
    log_time: The specific point in time to evaluate.
    full_df: Dataframe containing all my caffeine consumption logs.

    Returns
    -------
    float: The total mg of caffeine at that timestamp.
    """
    # Filter drinks consumed before the current log
    past_drinks = full_df[full_df['timestamp'] < log_time]
    
    total_at_time = 0
    # Citation: https://www.geeksforgeeks.org/pandas/pandas-dataframe-iterrows/
    for x, drink in past_drinks.iterrows():
        # Calculate time between drink and the specific log event using hours_passed function
        hrs = hours_passed(drink['timestamp'], log_time)
        # Add decayed amount of drink caffeine to total
        total_at_time = total_at_time + calculate_decay(drink['caffeine_mg'], hrs)
        
    return total_at_time


def minutes_until_threshold(current_mg, threshold_mg, half_life=5.0):
    """
    Predicts how many minutes until caffeine levels decay to my crashing threshold.
    Parameters
    ----------
    current_mg (float): The current amount of caffeine in the system.
    threshold_mg (float): The target caffeine level (the 'crash' point).
    half_life (float): The half-life of caffeine in hours, which according to MedicalNewsToday is usually 5 hrs.

    Returns
    -------
    float: Minutes remaining until the threshold is reached. Returns 0 if already below the threshold.
    """
    # Logarithmic calculation to find time remaining: hours = half_life * log(threshold / current) / log(0.5)
    if current_mg <= threshold_mg:
        return 0
    hours = half_life * math.log(threshold_mg / current_mg, 0.5)
    return round(hours * 60, 1)
