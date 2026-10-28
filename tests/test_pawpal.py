from datetime import date
from pawpal_system import Task, Pet

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