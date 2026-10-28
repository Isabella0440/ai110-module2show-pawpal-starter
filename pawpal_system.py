from dataclasses import dataclass, field
from datetime import date, timedelta
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
        """Sort tasks by their scheduled time."""
        pass

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> list[Task]:
        """Filter tasks by pet name or completion status."""
        pass

    def detect_conflicts(self) -> list[str]:
        """Identify tasks scheduled at conflicting times."""
        pass

    def mark_task_complete(self, task: Task):
        """Complete a task and handle recurring activities."""
        pass