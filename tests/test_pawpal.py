from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler

def test_task_completion():
    """Verify that marking a task complete updates its status."""

    # Create a new task
    task = Task(
        description="Morning Walk",
        time="08:00",
        due_date=date.today(),
        duration=30,
        priority="High",
        frequency="Daily"
    )

    # Verify that the task starts as incomplete
    assert task.completed is False

    # Mark the task as complete
    task.mark_complete()

    # Verify that the completion status changed
    assert task.completed is True

def test_task_addition():
    """Verify that adding a task increases a pet's task count."""

    # Create a pet
    pet = Pet(
        name="Bella",
        species="Dog",
        age=3
    )

    # Verify that the pet initially has no tasks
    assert len(pet.tasks) == 0

    # Create a new care task
    task = Task(
        description="Breakfast",
        time="09:00",
        due_date=date.today(),
        duration=15,
        priority="Medium",
        frequency="Daily"
    )

    # Add the task to the pet
    pet.add_task(task)

    # Verify that the task count increased
    assert len(pet.tasks) == 1

    # Verify that the correct task was added
    assert pet.tasks[0] is task
def test_chronological_sorting():
    """Verify tasks are sorted by due date and scheduled time."""

    owner = Owner("Isabella")
    scheduler = Scheduler(owner)

    tasks = [
        Task("Evening Walk", "18:00", date(2026, 10, 29)),
        Task("Breakfast", "09:00", date(2026, 10, 28)),
        Task("Morning Walk", "08:00", date(2026, 10, 28)),
        Task("Medication", "10:00", date(2026, 10, 29))
    ]

    sorted_tasks = scheduler.sort_by_time(tasks)

    descriptions = [task.description for task in sorted_tasks]

    assert descriptions == [
        "Morning Walk",
        "Breakfast",
        "Medication",
        "Evening Walk"
    ]
def test_task_filtering():
    """Verify tasks can be filtered by pet and completion status."""

    # Create an owner and two pets
    owner = Owner("Isabella")
    bella = Pet("Bella", "Dog", 3)
    luna = Pet("Luna", "Cat", 2)

    owner.add_pet(bella)
    owner.add_pet(luna)

    # Create three tasks
    walk = Task("Morning Walk", "08:00", date(2026, 10, 28))
    breakfast = Task("Breakfast", "09:00", date(2026, 10, 28))
    medication = Task("Medication", "10:00", date(2026, 10, 28))

    # Assign tasks to pets
    bella.add_task(walk)
    luna.add_task(breakfast)
    bella.add_task(medication)

    # Complete Bella's morning walk
    walk.mark_complete()

    scheduler = Scheduler(owner)

    # Test filtering by pet name
    bella_tasks = scheduler.filter_tasks(pet_name="Bella")

    assert len(bella_tasks) == 2
    assert [task.description for task in bella_tasks] == [
        "Morning Walk",
        "Medication"
    ]

    # Test filtering completed tasks
    completed_tasks = scheduler.filter_tasks(completed=True)

    assert len(completed_tasks) == 1
    assert completed_tasks[0].description == "Morning Walk"

    # Test filtering pending tasks
    pending_tasks = scheduler.filter_tasks(completed=False)

    assert len(pending_tasks) == 2
    assert [task.description for task in pending_tasks] == [
        "Breakfast",
        "Medication"
    ]

    # Test combining pet and completion filters
    bella_pending = scheduler.filter_tasks(
        pet_name="Bella",
        completed=False
    )

    assert len(bella_pending) == 1
    assert bella_pending[0].description == "Medication"
def test_daily_recurrence():
    """Verify daily tasks generate the next day's occurrence."""

    owner = Owner("Isabella")
    pet = Pet("Bella", "Dog", 3)
    owner.add_pet(pet)

    task = Task(
        description="Morning Walk",
        time="08:00",
        due_date=date(2026, 10, 28),
        duration=30,
        priority="High",
        frequency="Daily"
    )

    pet.add_task(task)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(task)

    assert task.completed is True
    assert len(pet.tasks) == 2

    next_task = pet.tasks[1]

    assert next_task.due_date == date(2026, 10, 29)
    assert next_task.completed is False
    assert next_task.description == "Morning Walk"
    assert next_task.time == "08:00"
def test_weekly_recurrence():
    """Verify weekly tasks generate an occurrence seven days later."""

    owner = Owner("Isabella")
    pet = Pet("Bella", "Dog", 3)
    owner.add_pet(pet)

    task = Task(
        description="Grooming",
        time="12:00",
        due_date=date(2026, 10, 28),
        duration=60,
        priority="Medium",
        frequency="Weekly"
    )

    pet.add_task(task)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(task)

    assert task.completed is True
    assert len(pet.tasks) == 2

    next_task = pet.tasks[1]

    assert next_task.due_date == date(2026, 11, 4)
    assert next_task.completed is False
    assert next_task.description == "Grooming"
def test_one_time_task():
    """Verify one-time tasks do not generate another occurrence."""

    owner = Owner("Isabella")
    pet = Pet("Bella", "Dog", 3)
    owner.add_pet(pet)

    task = Task(
        description="Veterinary Appointment",
        time="14:00",
        due_date=date(2026, 10, 28),
        duration=60,
        priority="High",
        frequency="Once"
    )

    pet.add_task(task)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(task)

    assert task.completed is True
    assert len(pet.tasks) == 1
    assert task.next_occurrence() is None
def test_overlapping_tasks():
    """Verify that overlapping tasks produce a conflict warning."""

    owner = Owner("Isabella")

    bella = Pet("Bella", "Dog", 3)
    luna = Pet("Luna", "Cat", 2)

    owner.add_pet(bella)
    owner.add_pet(luna)

    # Bella's walk runs from 8:00 to 8:30 AM
    walk = Task(
        description="Morning Walk",
        time="08:00",
        due_date=date(2026, 10, 28),
        duration=30
    )

    # Luna's breakfast runs from 8:15 to 8:30 AM
    breakfast = Task(
        description="Breakfast",
        time="08:15",
        due_date=date(2026, 10, 28),
        duration=15
    )

    bella.add_task(walk)
    luna.add_task(breakfast)

    scheduler = Scheduler(owner)

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "Morning Walk" in conflicts[0]
    assert "Breakfast" in conflicts[0]
def test_nonoverlapping_tasks():
    """Verify that back-to-back tasks do not produce conflicts."""

    owner = Owner("Isabella")
    bella = Pet("Bella", "Dog", 3)

    owner.add_pet(bella)

    # Morning walk ends at 8:30 AM
    walk = Task(
        description="Morning Walk",
        time="08:00",
        due_date=date(2026, 10, 28),
        duration=30
    )

    # Breakfast begins exactly at 8:30 AM
    breakfast = Task(
        description="Breakfast",
        time="08:30",
        due_date=date(2026, 10, 28),
        duration=15
    )

    bella.add_task(walk)
    bella.add_task(breakfast)

    scheduler = Scheduler(owner)

    conflicts = scheduler.detect_conflicts()

    assert conflicts == []
def test_empty_schedule():
    """Verify the scheduler handles an owner with no tasks."""

    owner = Owner("Isabella")
    scheduler = Scheduler(owner)

    assert scheduler.get_schedule() == []
    assert scheduler.sort_by_time([]) == []
    assert scheduler.filter_tasks() == []
    assert scheduler.detect_conflicts() == []
def test_duplicate_task_completion():
    """Verify completing the same task twice does not create duplicates."""

    owner = Owner("Isabella")
    pet = Pet("Bella", "Dog", 3)
    owner.add_pet(pet)

    task = Task(
        description="Morning Walk",
        time="08:00",
        due_date=date(2026, 10, 28),
        duration=30,
        frequency="Daily"
    )

    pet.add_task(task)

    scheduler = Scheduler(owner)

    # Complete the task for the first time
    scheduler.mark_task_complete(task)

    assert task.completed is True
    assert len(pet.tasks) == 2

    # Attempt to complete the same task again
    scheduler.mark_task_complete(task)

    # No additional recurring task should be created
    assert len(pet.tasks) == 2
    assert pet.tasks[1].due_date == date(2026, 10, 29)
def test_completed_tasks_do_not_conflict():
    """Verify completed tasks are excluded from conflict detection."""

    owner = Owner("Isabella")
    pet = Pet("Bella", "Dog", 3)
    owner.add_pet(pet)

    walk = Task(
        description="Morning Walk",
        time="08:00",
        due_date=date(2026, 10, 28),
        duration=30
    )

    breakfast = Task(
        description="Breakfast",
        time="08:15",
        due_date=date(2026, 10, 28),
        duration=15
    )

    pet.add_task(walk)
    pet.add_task(breakfast)

    scheduler = Scheduler(owner)

    # Confirm the tasks initially conflict
    assert len(scheduler.detect_conflicts()) == 1

    # Complete the morning walk
    scheduler.mark_task_complete(walk)

    # Completed activities should no longer trigger conflicts
    assert scheduler.detect_conflicts() == []