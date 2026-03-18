import datetime
from my_module.functions import calculate_decay, minutes_until_threshold, hours_passed


class CaffeineTracker:
    """
    A class to track caffeine consumption and predict crashes based on decay calculations.
    Attributes
    ----------
    half_life (float): The half-life of caffeine in hours (usually 5.0).
    crash_threshold (float): The caffeine level (mg) at which focus begins to fall off.
    energy_log (list): A list of dictionaries storing drink names, caffeine amounts, and timestamps.
    """
    
    def __init__(self, half_life=5.0, crash_threshold=40.0):
        """
        Initialize the tracker with metabolic parameters.
        """
        self.half_life = half_life
        self.crash_threshold = crash_threshold
        self.energy_log = []

    
    def add_drink(self, drink_name, mg_amount, time_consumed=None):
        """
        Adds a new drink entry to the log.
        Parameters
        ----------
        drink_name (str): Name of the drink.
        mg_amount (float): Amount of caffeine in mg.
        time_consumed: The time I drank it.
        """
        # Changing times to PST
        now = datetime.datetime.now() - datetime.timedelta(hours=7)
        if time_consumed is None:
            time_consumed = datetime.datetime.now()
        entry = {
            'drink': drink_name,
            'mg': mg_amount,
            'time': time_consumed
        }
        self.energy_log.append(entry)
        # Calculate how long ago it was drank
        total_hours = hours_passed(time_consumed, now)
        days_ago = int(total_hours // 24)
        if days_ago == 0:
            time_str = "today"
        elif days_ago == 1:
            time_str = "1 day ago"
        else:
            time_str = f"{days_ago} days ago"
        print(f"Logged {mg_amount}mg from {drink_name} {time_str}")

    
    def get_total_current_caffeine(self, now_pst=None):
        """
        Calculates the caffeine in body from all drinks logged.
        Parameters
        ----------
        now_pst: The current time in PST.

        Returns
        -------
        float: Total mg of caffeine left in my body.
        """
        if now_pst is None:
            now_pst = datetime.datetime.now() - datetime.timedelta(hours=7)
            
        total_now = 0
        now = datetime.datetime.now() - datetime.timedelta(hours=7)
        for entry in self.energy_log:
            # Calculate hours passed since this specific drink
            time_diff = now - entry['time']
            hours_passed = time_diff.total_seconds() / 3600
            # Apply decay based on the time passed
            remaining = calculate_decay(entry['mg'], hours_passed, self.half_life)
            total_now = total_now + remaining
        return round(total_now, 2)

    
    def predict_crash(self, now_pst=None):
        """
        Predicts when my caffeine levels will fall below my crash threshold.
        Parameters
        ----------
        now_pst: The current time in PST.

        Returns
        -------
        str: A written prediction of how much focus time I should have left.
        """
        if now_pst is None:
            import datetime
            # Citation: https://www.geeksforgeeks.org/python/working-with-datetime-objects-and-timezones-in-python/
            now_pst = datetime.datetime.now() - datetime.timedelta(hours=7)
        current_mg = self.get_total_current_caffeine(now_pst)
        minutes = minutes_until_threshold(
            current_mg, 
            self.crash_threshold, 
            self.half_life
        )
        if minutes <= 0:
            return f"You have reached the threshold and should feel/be feeling a crash soon!"
        return f"You have approximately {minutes} minutes of focus left."
