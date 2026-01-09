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
- Linux/macOS (for `select` module) or Windows (fallback mode available)

### Run the program
```bash
python clockClaude.py
```

## Usage

### Main Menu
When you start the program, you'll see:
```
    GRANDMA JEANNINE'S CLOCK

  [1] Interactive Clock with settings
  [2] Simple Clock without settings (Ctrl+C to stop)
  [Q] Quit
```

### Interactive Commands
While the clock is running, you can use these commands:

| Key | Action |
|-----|--------|
| `S` | Set the time |
| `A` | Set an alarm |
| `M` | Toggle 12h/24h mode |
| `P` | Pause/Resume the clock |
| `C` | Clear the alarm |
| `Q` | Quit the program |

---

## Technical Documentation: The `select` Module

### The Problem: Blocking Input

In a typical clock program, you might write:
```python
while True:
    display_time()
    time.sleep(1)
    command = input("Enter command: ")  # PROBLEM: Clock stops here!
```

The `input()` function is **blocking** — the program stops and waits for the user to press Enter. This means the clock would freeze every second waiting for input.

### The Solution: `select.select()`

The `select` module allows us to check if input is available **without blocking** the program.

```python
import select
import sys

# Wait for input OR timeout after 1 second
ready, _, _ = select.select([sys.stdin], [], [], 1)

if ready:
    # User typed something — read it
    command = sys.stdin.readline().strip()
else:
    # No input — continue with the clock
    pass
```

### How `select.select()` Works

```python
select.select(read_list, write_list, error_list, timeout)
```

| Parameter | Description |
|-----------|-------------|
| `read_list` | List of file descriptors to monitor for input (we use `[sys.stdin]`) |
| `write_list` | List of file descriptors to monitor for output (we use `[]`) |
| `error_list` | List of file descriptors to monitor for errors (we use `[]`) |
| `timeout` | Maximum time to wait in seconds (we use `1` for 1 second) |

**Returns:** Three lists of file descriptors that are ready. We only care about the first one (readable inputs).

### In Our Code

```python
# From run_clock() function:
ready, _, _ = select.select([sys.stdin], [], [], 1)

if ready:
    # Input is available — read the command
    command = sys.stdin.readline().strip().upper()
    # Process command...
else:
    # No input after 1 second — update the clock
    if not is_paused:
        current_time = increment_time(current_time)
```

### Platform Compatibility

- **Linux/macOS**: `select` works with `sys.stdin`
- **Windows**: `select` does NOT work with `sys.stdin` on Windows

Our code includes a fallback for Windows:
```python
except (ImportError, OSError):
    # Fallback for Windows — simple sleep without interactive input
    time.sleep(1)
    if not is_paused:
        current_time = increment_time(current_time)
```

---

## Architecture

### Design Principles

1. **Separation of Concerns**: Each function has ONE job
2. **Future-Proof**: Easy to replace time source (e.g., with an API)
3. **No Classes**: Functions only (appropriate for Bachelor 1st year)
4. **Well-Commented**: Every function has a docstring explaining its purpose

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
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ check_alarm()   │  │ set_alarm()     │  │ clear_alarm()│ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
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

| Function | Layer | Purpose |
|----------|-------|---------|
| `display_time()` | Presentation | Shows clock on screen |
| `clear_screen()` | Presentation | Clears terminal |
| `get_time_input()` | Presentation | Prompts user for time |
| `format_time_24h()` | Service | Formats tuple to `hh:mm:ss` |
| `format_time_12h()` | Service | Formats tuple to `hh:mm:ss AM/PM` |
| `check_alarm()` | Service | Compares current time with alarm |
| `set_alarm()` | Service | Sets alarm time |
| `clear_alarm()` | Service | Removes alarm |
| `toggle_pause()` | Service | Pauses/resumes clock |
| `toggle_display_mode()` | Service | Switches 12h/24h |
| `set_time()` | Core | Sets current time |
| `increment_time()` | Core | Adds 1 second to time |
| `run_clock()` | Main | Main loop |

---

## Future Improvements

- Graphical interface with `tkinter` or `pygame`
- External API for time synchronization
- Multiple alarm support
- Sound notification for alarm

---

## Author

**Rayene, Jean-Pierre, Claude** — Bachelor 1st Year, Data-AI, La Plateforme

