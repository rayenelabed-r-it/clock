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
║                          clear_alarm()         _mode()        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
                              │
                              ▼ uses
╔═══════════════════════════════════════════════════════════════╗
║                     DOMAIN LAYER                              ║
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
║                      SOURCE LAYER                             ║
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
│                      run_clock()                            │
│                     (Main Loop)                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. Initialize with time.localtime()                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────┐
         │          WHILE TRUE LOOP           │
         └────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
      ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
      │display_time()│ │check_alarm() │ │select.select │
      │              │ │              │ │(wait 1s)     │
      └──────────────┘ └──────────────┘ └──────┬───────┘
                                               │
                              ┌────────────────┴────────────────┐
                              ▼                                 ▼
                    ┌─────────────────┐              ┌─────────────────┐
                    │ Input detected? │              │ No input        │
                    │ → Process       │              │ → increment_    │
                    │   command       │              │   time()        │
                    └─────────────────┘              └─────────────────┘
```

---

## Function Reference Table

| Function                      | Input                 | Output                | Responsibility        |
|----------                     |-------                |--------               |----------------       |
| `format_time_24h(tuple)`      | `(16, 30, 0)`         | `"16:30:00"`          | 24h formatting        |
| `format_time_12h(tuple)`      | `(16, 30, 0)`         | `"04:30:00 PM"`       | 12h formatting        |
| `set_time(tuple)`             | `(16, 30, 0)`         | `True/False`          | Modify time           |
| `increment_time(tuple)`       | `(16, 30, 59)`        | `(16, 31, 0)`         | +1 second             |
| `check_alarm(tuple)`          | current time          | `True/False`          | Check alarm           |
| `set_alarm(tuple)`            | `(7, 0, 0)`           | `True/False`          | Set alarm             |

---

## Why This Architecture?

### Benefits for the oral defense:

1. **Explainable**: "This function does X, that one does Y"
2. **Testable**: You can test `format_time_24h()` in isolation
3. **Maintainable**: Display bug? → Look at `display_time()` only
4. **Extensible**: Change the source = modify ONE function

### Example defense Q&A:

> **Jury**: "Why did you separate formatting from display?"
>
> **You**: "To be able to reuse formatting elsewhere. For example, `check_alarm()` also uses formatting to show the alarm time, without duplicating code."

---

## The `select` Library in Brief

**Problem**: `input()` blocks the program — the clock stops.

**Solution**: `select.select()` waits for 1 second. If the user types something, we process it. Otherwise, we continue.

```python
ready, _, _ = select.select([sys.stdin], [], [], 1)
#                           ▲           ▲   ▲   ▲
#                           │           │   │   └─ timeout: 1 second
#                           │           │   └─ error list (empty)
#                           │           └─ write list (empty)
#                           └─ read list (keyboard input)
```

**Result**: The clock keeps running even if the user does nothing.
