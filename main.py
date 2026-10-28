from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    """Demonstrate the core functionality of PawPal+."""

    # Step 1: Create an owner
    owner = Owner("Isabella")

    # Step 2: Create two pets
    bella = Pet("Bella", "Dog", 3)
    luna = Pet("Luna", "Cat", 2)

    # Step 3: Register pets with the owner
    owner.add_pet(bella)
    owner.add_pet(luna)

    # Step 4: Create care tasks
    task1 = Task(
        description="Morning Walk",
        time="08:00",
        due_date=date.today(),
        duration=30,
        priority="High",
        frequency="Daily"
    )

    task2 = Task(
        description="Breakfast",
        time="09:00",
        due_date=date.today(),
        duration=15,
        priority="Medium",
        frequency="Daily"
    )

    task3 = Task(
        description="Medication",
        time="10:00",
        due_date=date.today(),
        duration=5,
        priority="High",
        frequency="Daily"
    )

    task4 = Task(
        description="Evening Walk",
        time="18:00",
        due_date=date.today(),
        duration=30,
        priority="Medium",
        frequency="Daily"
    )

    # Step 5: Assign tasks to pets
    bella.add_task(task1)
    bella.add_task(task4)

    luna.add_task(task2)
    luna.add_task(task3)

    # Step 6: Initialize the scheduler
    scheduler = Scheduler(owner)

    # Step 7: Retrieve and display today's schedule
    schedule = scheduler.get_schedule()

    print("\n" + "=" * 55)
    print("                 PAWPAL+")
    print("              TODAY'S SCHEDULE")
    print("=" * 55)

    print(f"Owner: {owner.name}")
    print(f"Date: {date.today().strftime('%B %d, %Y')}")
    print(f"Registered Pets: {len(owner.pets)}")
    print("-" * 55)

    # Sort tasks for display
    for task in sorted(schedule, key=lambda t: t.time):

        # Find which pet owns the task
        pet_name = "Unknown"

        for pet in owner.pets:
            if task in pet.tasks:
                pet_name = pet.name
                break

        status = "Completed" if task.completed else "Pending"

        print(f"Time: {task.time}")
        print(f"Pet: {pet_name}")
        print(f"Activity: {task.description}")
        print(f"Duration: {task.duration} minutes")
        print(f"Priority: {task.priority}")
        print(f"Frequency: {task.frequency}")
        print(f"Status: {status}")
        print("-" * 55)

    print(f"Total Tasks: {len(schedule)}")
    print("=" * 55)


if __name__ == "__main__":
    main()