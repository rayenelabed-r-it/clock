# GRANDMA JEANNINE'S CLOCK
# A clock program with alarm, 12h/24h display modes, and pause feature.



# IMPORTS

# time module: time.sleep() pauses program, time.localtime() gets time
import time

# os module: os.system() runs shell commands, os.name identifies the OS
import os


# GLOBAL VARIABLES - Store the clock's state, accessible from all functions

# Current time as tuple (hours, minutes, seconds)
# Example: (14, 30, 45) = 14:30:45
current_time = (0, 0, 0)

# Alarm time as tuple (hours, minutes, seconds). None = no alarm set
alarm_time = None

# Display mode: True = 24h format, False = 12h format (AM/PM)
is_24h_mode = True

# Pause state: True = clock frozen, False = clock running
is_paused = False


# DISPLAY FUNCTIONS

# clear_screen()
# Clears terminal using 'cls' (Windows) or 'clear' (Linux/Mac)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# display_time(time_tuple)
# Shows the clock on screen with current time, alarm, and status
# Parameter: time_tuple = (hours, minutes, seconds)
def display_time(time_tuple):
    clear_screen()

    # Tuple unpacking: (14, 30, 45) becomes hours=14, minutes=30...
    hours, minutes, seconds = time_tuple

    print("\n    GrandMa Jeannine's Clock\n")

    if is_24h_mode:
        # :02d = pad with zeros, 2 digits minimum. So 5 becomes "05"
        print(f"        {hours:02d}:{minutes:02d}:{seconds:02d}")
        print("        (24h mode)\n")
    else:
        # 12h conversion rules:
        # 0h=12AM, 1-11h=AM, 12h=12PM, 13-23h=PM (-12h)
        if hours == 0:
            display_hours = 12
            period = "AM"
        elif hours < 12:
            display_hours = hours
            period = "AM"
        elif hours == 12:
            display_hours = 12
            period = "PM"
        else:
            display_hours = hours - 12
            period = "PM"

        print(f"        {display_hours:02d}:{minutes:02d}:{seconds:02d} {period}")
        print("        (12h mode)\n")

    if is_paused:
        print("        [PAUSED]\n")

    if alarm_time is not None:
        h, m, s = alarm_time
        print(f"        Alarm set: {h:02d}:{m:02d}:{s:02d}\n")

    # Show hint to access menu
    print("    Press Ctrl+C to open menu")


# TIME MANAGEMENT FUNCTIONS

# set_time(time_tuple)
# Sets the clock time after validating the input
# Parameter: time_tuple = (hours, minutes, seconds)
# Returns True if valid, False otherwise
def set_time(time_tuple):
    # 'global' needed to modify global variable (else creates local copy)
    global current_time

    hours, minutes, seconds = time_tuple

    # Validate ranges: hours 0-23, minutes 0-59, seconds 0-59
    if not (0 <= hours <= 23):
        print("Error: hours must be between 0 and 23")
        return False

    if not (0 <= minutes <= 59):
        print("Error: minutes must be between 0 and 59")
        return False

    if not (0 <= seconds <= 59):
        print("Error: seconds must be between 0 and 59")
        return False

    current_time = (hours, minutes, seconds)
    return True


# increment_time(time_tuple)
# Adds one second and handles overflow (60s->1min, 60min->1h, 24h->0)
# Parameter: time_tuple = (hours, minutes, seconds)
# Returns new tuple with incremented time
def increment_time(time_tuple):
    hours, minutes, seconds = time_tuple

    seconds += 1

    # Cascade overflow: seconds -> minutes -> hours -> midnight
    if seconds >= 60:
        seconds = 0
        minutes += 1
        if minutes >= 60:
            minutes = 0
            hours += 1
            if hours >= 24:
                hours = 0

    # Return new tuple (immutable, cannot modify original)
    return (hours, minutes, seconds)


# ALARM FUNCTIONS

# set_alarm(time_tuple)
# Sets alarm time after validation. Shows message when time matches
# Parameter: time_tuple = (hours, minutes, seconds)
# Returns True if valid, False otherwise
def set_alarm(time_tuple):
    global alarm_time

    hours, minutes, seconds = time_tuple

    if not (0 <= hours <= 23):
        print("Error: hours must be between 0 and 23")
        return False

    if not (0 <= minutes <= 59):
        print("Error: minutes must be between 0 and 59")
        return False

    if not (0 <= seconds <= 59):
        print("Error: seconds must be between 0 and 59")
        return False

    alarm_time = (hours, minutes, seconds)
    print(f"    Alarm set for {hours:02d}:{minutes:02d}:{seconds:02d}")
    return True


# check_alarm()
# Compares current_time with alarm_time, displays message if match
# Returns True if alarm triggered, False otherwise
# Clears alarm after triggering
def check_alarm():
    global alarm_time

    # Both conditions: alarm exists AND times match exactly
    if alarm_time is not None and current_time == alarm_time:
        print("\n" + "=" * 50)
        print("        WAKE UP GRANDMA JEANNINE!")
        print("        It's time to wake up!")
        print("=" * 50 + "\n")

        # Clear alarm so it doesn't ring every second
        alarm_time = None
        return True

    return False


# DISPLAY MODE AND PAUSE FUNCTIONS

# toggle_display_mode()
# Switches between 12h and 24h format using 'not' operator
def toggle_display_mode():
    global is_24h_mode
    # not True = False, not False = True
    is_24h_mode = not is_24h_mode


# toggle_pause() - Freezes or unfreezes the clock
def toggle_pause():
    global is_paused
    is_paused = not is_paused


# INPUT FUNCTIONS

# get_time_input(prompt)
# Asks user to enter hours, minutes, seconds separately
# Parameter: prompt = message to display
# Returns tuple (h, m, s) or None if invalid input
def get_time_input(prompt):
    print(f"\n    {prompt}\n")

    # try/except catches ValueError when int() fails
    # Example: int("abc") raises ValueError
    try:
        # input() returns string, int() converts to integer
        hours = int(input("    Hours (0-23): "))
        minutes = int(input("    Minutes (0-59): "))
        seconds = int(input("    Seconds (0-59): "))
        return (hours, minutes, seconds)
    except ValueError:
        print("    Error: please enter valid numbers")
        return None


# show_menu() - Displays the configuration menu
def show_menu():
    print("\n    MENU")
    print("[1] Set time         [2] Set alarm       [3] Toggle 12h/24h mode")
    print("[4] Pause/Resume     [5] Start clock     [6] Quit")
    print()


# run_clock()
# Runs the clock indefinitely until user presses Ctrl+C
# Updates time every second and checks alarm
def run_clock():
    global current_time

    # Infinite loop - runs until KeyboardInterrupt (Ctrl+C)
    while True:
        # Display current time
        display_time(current_time)

        # Check if alarm should ring
        if check_alarm():
            # Pause to let user see the alarm message
            time.sleep(30)

        # Wait 1 second (clock tick)
        time.sleep(1)

        # Increment time if not paused
        if not is_paused:
            current_time = increment_time(current_time)


# MAIN PROGRAM

# main()
# Main function: shows menu, then runs clock indefinitely
# Ctrl+C returns to menu, allowing reconfiguration
def main():
    global current_time

    # Initialize with system time using time.localtime() structure
    now = time.localtime()
    current_time = (now.tm_hour, now.tm_min, now.tm_sec)

    # Main loop - menu -> clock -> menu (on Ctrl+C)
    while True:
        clear_screen()
        print("\n    Welcome to GrandMa Jeannine's Clock!\n")

        # Show current settings
        hours, minutes, seconds = current_time
        print(f"    Current time: {hours:02d}:{minutes:02d}:{seconds:02d}")

        if alarm_time is not None:
            ah, am, asec = alarm_time
            print(f"    Alarm: {ah:02d}:{am:02d}:{asec:02d}")
        else:
            print("    Alarm: not set")

        mode = "24h" if is_24h_mode else "12h"
        print(f"    Mode: {mode}")

        status = "paused" if is_paused else "running"
        print(f"    Status: {status}")

        # Display menu
        show_menu()

        # Get user choice
        choice = input("    Your choice: ").strip()

        if choice == "1":
            # Set time
            new_time = get_time_input("Set the time:")
            if new_time and set_time(new_time):
                print("\n    Time updated!")
                time.sleep(1)

        elif choice == "2":
            # Set alarm
            new_alarm = get_time_input("Set the alarm:")
            if new_alarm:
                set_alarm(new_alarm)
                time.sleep(1)

        elif choice == "3":
            # Toggle display mode
            toggle_display_mode()
            mode = "24h" if is_24h_mode else "12h"
            print(f"\n    Display mode: {mode}")
            time.sleep(1)

        elif choice == "4":
            # Pause/Resume
            toggle_pause()
            status = "paused" if is_paused else "running"
            print(f"\n    Clock is now {status}")
            time.sleep(1)

        elif choice == "5":
            # Start clock - runs indefinitely until Ctrl+C
            print("\n    Starting clock... (Press Ctrl+C to return to menu)")
            time.sleep(1)
            try:
                run_clock()
            except KeyboardInterrupt:
                # Ctrl+C pressed - return to menu
                print("\n\n    Returning to menu...")
                time.sleep(1)

        elif choice == "6":
            # Quit
            print("\n    Goodbye GrandMa Jeannine!")
            print("    See you soon!\n")
            break


# ENTRY POINT
# __name__ == "__main__" is True only when running directly
# (not when imported as a module)
if __name__ == "__main__":
    main()
