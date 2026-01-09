# Grandma Jeannine's Clock


## Features

### Required Features
- **Time Display**: Shows current time in `hh:mm:ss` format, updating every second
- **Set Time**: Manually set the clock time using a tuple `(hours, minutes, seconds)`
- **Alarm**: Set an alarm that triggers a notification when the time is reached

### Bonus Features
- **12h/24h Mode**: Toggle between 24-hour format and 12-hour AM/PM format
- **Pause/Resume**: Pause the clock to play tricks on grandma!

## Installation

### Requirements
- Python 3.x
- Linux/macOS or Windows

### Run the program
```bash
python clock.py
```

## Usage

### Main Menu
When you start the program, you'll see:
```
    Welcome to GrandMa Jeannine's Clock!

    Current time: 14:30:45
    Alarm: not set
    Mode: 24h
    Status: running

    MENU
[1] Set time         [2] Set alarm       [3] Toggle 12h/24h mode
[4] Pause/Resume     [5] Start clock     [6] Quit
```

### Menu Options

| Option            | Action                                                |
|--------           |--------                                               |
| `1`               | Set the clock time manually                           |
| `2`               | Set an alarm                                          |
| `3`               | Toggle between 12h and 24h display mode               |
| `4`               | Pause or resume the clock                             |
| `5`               | Start the clock (press `Ctrl+C` to return to menu)    |
| `6`               | Quit the program                                      |

---

## Architecture

### Function Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ display_time()  │  │ clear_screen()  │  │ get_time_    │ │
│  │                 │  │                 │  │ input()      │ │
│  └────────┬────────┘  └─────────────────┘  └──────────────┘ │
└───────────┼─────────────────────────────────────────────────┘
            │ uses
┌───────────▼─────────────────────────────────────────────────┐
│                     SERVICE LAYER                           │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │ format_time_24h │  │ format_time_12h │                   │
│  └─────────────────┘  └─────────────────┘                   │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │ check_alarm()   │  │ set_alarm()     │                   │
│  └─────────────────┘  └─────────────────┘                   │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │ toggle_pause()  │  │ toggle_display_ │                   │
│  │                 │  │ mode()          │                   │
│  └─────────────────┘  └─────────────────┘                   │
└───────────┼─────────────────────────────────────────────────┘
            │ uses
┌───────────▼─────────────────────────────────────────────────┐
│                   CORE/DOMAIN LAYER                         │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │ set_time()      │  │ increment_time()│                   │
│  └─────────────────┘  └─────────────────┘                   │
│                                                             │
│  Global State: current_time, alarm_time, is_24h_mode,       │
│                is_paused                                    │
└───────────┼─────────────────────────────────────────────────┘
            │ uses
┌───────────▼─────────────────────────────────────────────────┐
│                    DATA/SOURCE LAYER                        │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ time.localtime() — Current implementation               ││
│  │ Future: API call to external time service               ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### Function Reference

| Function                  | Layer                 | Purpose                                                       |
|----------                 |-------                |---------                                                      |
| `display_time()`          | Presentation          | Shows clock on screen                                         |
| `clear_screen()`          | Presentation          | Clears terminal                                               |
| `get_time_input()`        | Presentation          | Prompts user for time                                         |
| `format_time_24h()`       | Service               | Formats tuple to `hh:mm:ss`                                   | 
| `format_time_12h()`       | Service               | Formats tuple to `hh:mm:ss AM/PM`                             |
| `check_alarm()`           | Service               | Compares current time with alarm (auto-clears after trigger)  |
| `set_alarm()`             | Service               | Sets alarm time                                               |
| `toggle_pause()`          | Service               | Pauses/resumes clock                                          |
| `toggle_display_mode()`   | Service               | Switches 12h/24h                                              |
| `set_time()`              | Core                  | Sets current time                                             |
| `increment_time()`        | Core                  | Adds 1 second to time                                         |
| `show_menu()`             | Presentation          | Displays the menu options                                     |
| `run_clock()`             | Main                  | Clock display loop                                            |
| `main()`                  | Main                  | Entry point, menu handling                                    |

---

## Future Improvements

- Graphical interface with `tkinter` or `pygame`
- External API for time synchronization
- Multiple alarm support
- Sound notification for alarm
- Using GitPages and GitAction

---

## Author

**Rayene, Jean-Pierre, Claude** — Bachelor 1st Year, Data-AI, La Plateforme

