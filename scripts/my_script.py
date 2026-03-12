import os
import csv
import pandas as pd
from datetime import datetime, timedelta

def log_caffeine_entry():
    """
    Quickly log a drink to into CSV file without opening the whole notebook
    """
    # Setup the file path to the correct CSV
    file_path = 'caffeine_log.csv'
    # Converting time to PST
    pst_now = datetime.now() - timedelta(hours=7)
    while True:
        user_choice = input("Do you want to add an entry to the dataframe? (yes/no): ").strip().lower()
        if user_choice not in ['yes', 'y']:
            break  # Ends the script
        drink = input("What did you just drink? (ex. Red Bull, Alani Nu, Coffee): ")
        try:
            caffeine_mg = float(input("How many mg of caffeine is it?"))
            focus = int(input("On a scale of 1-10, how focused/tired are you right now? "))
            if not (1 <= focus <= 10):
                print("Focus must be in between 1 and 10.")
        except ValueError:
            print("Please enter numbers only.")
            continue
        # Create the data entry
        new_entry = {
            'timestamp': pst_now.strftime('%Y-%m-%d %H:%M'),
            'drink': drink,
            'caffeine_mg': caffeine_mg,
            'focus_after_one_hr': focus
        }
        # Convert to DataFrame
        df_new = pd.DataFrame([new_entry])
        # Check for file existence to handle the header
        file_exists = os.path.isfile(file_path)
        # Make sure no parser errors
        if file_exists:
            with open(file_path, 'a+') as f:
                f.seek(0, 2)          # Go to the end of the file
                if f.tell() > 0:      # If the file isn't empty
                    f.seek(f.tell() - 1) # Look at the very last character
                    if f.read(1) != '\n': # If it's not a newline
                        f.write('\n')      # Add one
        # Append/add entry to the CSV
        df_new.to_csv(
            file_path, 
            mode='a', 
            index=False, 
            header=not file_exists,
            # quoting=csv.QUOTE_NONNUMERIC wraps the drink name in "quotes" so commas won't cause ParserErrors later
            quoting=csv.QUOTE_NONNUMERIC
        )
        print(f"Logged! {drink} with {caffeine_mg} mg is tracked.")
        # Ask to continue
        choice = input("Would you like to add another entry? (y/n): ").lower()
        if choice != 'y':
            print("Done logging. Check your notebook to reload the data!")
            break
            
if __name__ == "__main__":
    log_caffeine_entry()