# Grandma Jeannine's Clock — Architecture Guide

Overview of the code architecture.

---

## Core Principle

> **Separate "where the time comes from" from "how it's displayed"**

Each function has **one single responsibility**.

---

## Layer Diagram

```
╔═══════════════════════════════════════════════════════════════╗
║                    PRESENTATION LAYER                         ║
║                     (User Interface)                          ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║   display_time()      clear_screen()      get_time_input()    ║
║   └─ Shows the        └─ Clears the       └─ Prompts user     ║
║      clock               terminal            for time         ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
                              │
                              ▼ uses
╔═══════════════════════════════════════════════════════════════╗
║                      SERVICE LAYER                            ║
║                    (Business Logic)                           ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║   FORMATTING             ALARM                 CONTROL        ║
║   ──────────             ─────                 ───────        ║
║   format_time_24h()      set_alarm()           toggle_pause() ║
║   format_time_12h()      check_alarm()         toggle_display ║
║                                                _mode()        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
                              │
                              ▼ uses
╔═══════════════════════════════════════════════════════════════╗
║                   CORE/DOMAIN LAYER                           ║
║                   (Time Management)                           ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║   set_time()                    increment_time()              ║
║   └─ Modifies current           └─ Adds 1 second              ║
║      time                          (handles overflow)         ║
║                                                               ║
║   ┌─────────────────────────────────────────────────────┐     ║
║   │ GLOBAL STATE (variables)                            │     ║
║   │ • current_time = (h, m, s)                          │     ║
║   │ • alarm_time = (h, m, s) or None                    │     ║
║   │ • is_24h_mode = True/False                          │     ║
║   │ • is_paused = True/False                            │     ║
║   └─────────────────────────────────────────────────────┘     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
                              │
                              ▼ uses
╔═══════════════════════════════════════════════════════════════╗
║                    DATA/SOURCE LAYER                          ║
║                    (Time Origin)                              ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║   TODAY:                       TOMORROW (future API):         ║
║   time.localtime()             api.get_time()                 ║
║   └─ System time               └─ Server time                 ║
║                                                               ║
║   The rest of the code doesn't change!                        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## Main Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│                        main()                               │
│                   (Entry Point)                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. Initialize with time.localtime()                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────┐
         │       MAIN MENU LOOP               │
         │  (show_menu → get choice)          │
         └────────────────────────────────────┘
                              │
         Choice 5: Start clock
                              │
                              ▼
         ┌────────────────────────────────────┐
         │          run_clock()               │
         │        WHILE TRUE LOOP             │
         └────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
      ┌──────────────┐                ┌──────────────┐
      │display_time()│                │check_alarm() │
      └──────────────┘                └──────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ time.sleep(1)   │
                    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ if not paused:  │
                    │ increment_time()│
                    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Ctrl+C pressed? │
                    │ → Return to     │
                    │   main menu     │
                    └─────────────────┘
```

---

## Function Reference Table

| Function                      | Input                 | Output                | Responsibility        |
|-------------------------------|-----------------------|-----------------------|-----------------------|
| `display_time(tuple)`         | `(16, 30, 0)`         | (none)                | Shows clock on screen |
| `clear_screen()`              | (none)                | (none)                | Clears terminal       |
| `get_time_input(prompt)`      | `"Set the time:"`     | `(h, m, s)` or `None` | Prompts user for time |
| `format_time_24h(tuple)`      | `(16, 30, 0)`         | `"16:30:00"`          | 24h formatting        |
| `format_time_12h(tuple)`      | `(16, 30, 0)`         | `"04:30:00 PM"`       | 12h formatting        |
| `set_time(tuple)`             | `(16, 30, 0)`         | `True/False`          | Modify time           |
| `increment_time(tuple)`       | `(16, 30, 59)`        | `(16, 31, 0)`         | +1 second             |
| `check_alarm()`               | (uses global)         | `True/False`          | Check & clear alarm   |
| `set_alarm(tuple)`            | `(7, 0, 0)`           | `True/False`          | Set alarm             |
| `toggle_pause()`              | (none)                | (none)                | Toggle pause state    |
| `toggle_display_mode()`       | (none)                | (none)                | Toggle 12h/24h        |
| `show_menu()`                 | (none)                | (none)                | Display menu          |
| `run_clock()`                 | (none)                | (none)                | Clock display loop    |
| `main()`                      | (none)                | (none)                | Entry point           |

---

## Why This Architecture?

1. **Explainable**: "This function does X, that one does Y"
2. **Testable**: You can test `format_time_24h()` in isolation
3. **Maintainable**: Display bug? → Look at `display_time()` only
4. **Extensible**: Change the source = modify ONE function

> **You**: "To be able to reuse formatting elsewhere. For example, `check_alarm()` also uses formatting to show the alarm time, without duplicating code."

