from dataclasses import dataclass, field
from datetime import date, timedelta, datetime
from typing import Optional
@dataclass
class Task:
    description: str
    time: str
    due_date: date
    duration: int = 0
    priority: str = "Medium"
    frequency: str = "Once"
    completed: bool = False

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def next_occurrence(self) -> Optional[date]:
        """Calculate the next date for a recurring task."""
        if self.frequency.lower() == "daily":
            return self.due_date + timedelta(days=1)

        elif self.frequency.lower() == "weekly":
            return self.due_date + timedelta(weeks=1)

        return None
@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task):
        """Remove a task from this pet."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> list[Task]:
        """Return all tasks belonging to this pet."""
        return self.tasks.copy()
@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's collection."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet):
        """Remove a pet from the owner's collection."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_all_tasks(self) -> list[Task]:
        """Retrieve tasks from all registered pets."""
        all_tasks = []

        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())

        return all_tasks
class Scheduler:
    def __init__(self, owner: Owner):
        """Initialize the scheduler with an owner."""
        self.owner = owner

    def get_schedule(self) -> list[Task]:
        """Retrieve all scheduled tasks from the owner."""
        return self.owner.get_all_tasks()

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks chronologically by due date and scheduled time."""
        return sorted(
            tasks,
            key=lambda task: (task.due_date, task.time)
        )

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> list[Task]:
        """Filter scheduled tasks by pet name and completion status."""

        filtered_tasks = []

        for pet in self.owner.pets:

            # Skip pets that do not match the requested name
            if pet_name is not None:
                if pet.name.lower() != pet_name.lower():
                    continue

            for task in pet.get_tasks():

                # Skip tasks that do not match the completion filter
                if completed is not None:
                    if task.completed != completed:
                        continue

                filtered_tasks.append(task)

        return self.sort_by_time(filtered_tasks)

    def detect_conflicts(self) -> list[str]:
        """Identify overlapping tasks scheduled on the same day."""

        conflicts = []

        # Only check tasks that have not been completed
        tasks = self.filter_tasks(completed=False)

        for i in range(len(tasks)):
            task1 = tasks[i]

            start1 = datetime.combine(
                task1.due_date,
                datetime.strptime(task1.time, "%H:%M").time()
            )

            end1 = start1 + timedelta(minutes=task1.duration)

            for j in range(i + 1, len(tasks)):
                task2 = tasks[j]

                start2 = datetime.combine(
                    task2.due_date,
                    datetime.strptime(task2.time, "%H:%M").time()
                )

                end2 = start2 + timedelta(minutes=task2.duration)

                # Check whether the time intervals overlap
                if start1 < end2 and start2 < end1:

                    conflict_message = (
                        f"Conflict: '{task1.description}' "
                        f"({task1.time}) overlaps with "
                        f"'{task2.description}' ({task2.time}) "
                        f"on {task1.due_date}."
                    )

                    conflicts.append(conflict_message)

        return conflicts

    def mark_task_complete(self, task: Task):
        """Complete a task and schedule its next occurrence if recurring."""

        # Find the pet that owns this task
        for pet in self.owner.pets:
            for existing_task in pet.tasks:

                if existing_task is task:

                    # Prevent completing the same task twice
                    if task.completed:
                        return

                    # Mark the current task as completed
                    task.mark_complete()

                    # Calculate the next occurrence
                    next_date = task.next_occurrence()

                    # Create a new task if the activity repeats
                    if next_date is not None:

                        new_task = Task(
                            description=task.description,
                            time=task.time,
                            due_date=next_date,
                            duration=task.duration,
                            priority=task.priority,
                            frequency=task.frequency
                        )

                        pet.add_task(new_task)

                    return