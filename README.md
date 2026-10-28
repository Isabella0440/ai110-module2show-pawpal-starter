# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

## Sample CLI Output

The following output demonstrates the core functionality of PawPal+
using the `main.py` script. The demonstration creates an owner,
registers two pets, assigns four care tasks, and displays the
daily schedule in chronological order.

To run the demonstration:

```bash
python3 main.py
```

### Example Output

```text
=======================================================
                 PAWPAL+
              TODAY'S SCHEDULE
=======================================================
Owner: Isabella
Date: October 28, 2026
Registered Pets: 2
-------------------------------------------------------
Time: 08:00
Pet: Bella
Activity: Morning Walk
Duration: 30 minutes
Priority: High
Frequency: Daily
Status: Pending
-------------------------------------------------------
Time: 09:00
Pet: Luna
Activity: Breakfast
Duration: 15 minutes
Priority: Medium
Frequency: Daily
Status: Pending
-------------------------------------------------------
Time: 10:00
Pet: Luna
Activity: Medication
Duration: 5 minutes
Priority: High
Frequency: Daily
Status: Pending
-------------------------------------------------------
Time: 18:00
Pet: Bella
Activity: Evening Walk
Duration: 30 minutes
Priority: Medium
Frequency: Daily
Status: Pending
-------------------------------------------------------
Total Tasks: 4
=======================================================
```

## 🧪 Testing PawPal+

PawPal+ uses pytest to verify the functionality of its core classes and scheduling algorithms.

### Running Automated Tests

Run the full test suite:

```bash
python3 -m pytest
```

### Test Coverage

| Test | Purpose | Result |
|------|---------|--------|
| Task completion | Verify tasks can be marked complete | Passed |
| Task addition | Verify tasks can be assigned to pets | Passed |
| Chronological sorting | Verify tasks are ordered by date and time | Passed |
| Task filtering | Verify filtering by pet and completion status | Passed |
| Daily recurrence | Verify daily tasks generate the next occurrence | Passed |
| Weekly recurrence | Verify weekly tasks generate the next occurrence | Passed |
| One-time tasks | Verify nonrecurring tasks do not repeat | Passed |
| Overlapping tasks | Verify scheduling conflicts are detected | Passed |
| Nonoverlapping tasks | Verify back-to-back activities do not conflict | Passed |
| Empty schedules | Verify the scheduler handles no tasks | Passed |
| Duplicate completion | Verify recurring tasks are not duplicated | Passed |
| Completed task conflicts | Verify completed tasks are excluded from conflicts | Passed |

### Verification Results

All 12 automated tests passed successfully using Python 3.14.7 and pytest 9.2.0.

Sample test output:

```text
collected 12 items

tests/test_pawpal.py ............ [100%]

12 passed in 0.03s
```

### Testing Limitations

The current automated tests focus on backend functionality, including task management, scheduling, recurrence, and conflict detection.

The Streamlit interface has been manually tested, but automated UI tests have not yet been implemented.

Future improvements could include additional input validation tests, persistent data storage tests, and more complex scheduling scenarios.

## 📐 Smarter Scheduling

PawPal+ uses scheduling algorithms to organize pet care activities, manage
recurring tasks, and identify scheduling conflicts.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks chronologically by due date and scheduled time using Python's `sorted()` function. |
| Filtering | `Scheduler.filter_tasks()` | Filters tasks by pet name, completion status, or both. Results are returned in chronological order. |
| Conflict handling | `Scheduler.detect_conflicts()` | Detects overlapping tasks by comparing their start and end times. Reports conflicts without automatically rescheduling activities. |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.mark_task_complete()` | Automatically creates the next occurrence when a daily or weekly task is completed through the Scheduler. One-time tasks do not repeat. |

### Scheduling Design Decisions

The scheduling algorithms are implemented in the `Scheduler` class rather
than directly in the Streamlit interface. This separates the application's
business logic from its user interface and makes the algorithms easier to
maintain, reuse, and test.

Chronological sorting prioritizes tasks based on their scheduled date and
time rather than their priority level. Priority is stored as task information
but does not currently affect the order of the schedule.

Conflict detection assumes that one owner is responsible for all pet care
activities. When two pending tasks overlap, the system identifies the conflict
but leaves the decision about rescheduling to the owner.

Recurring tasks are generated when their previous occurrence is marked
complete through the Scheduler. This prevents unnecessary duplicate tasks
and preserves completed activities as part of the task history.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

