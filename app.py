import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Initialize the application's session data
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Pet Owner")

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(st.session_state.owner)

st.title("🐾 PawPal+")

st.markdown(
    """
    Welcome to **PawPal+**, your personal pet care management assistant!

    Keep track of your pets, organize their daily routines, and manage
    activities such as feeding, walking, medications, and appointments.

    Add your pets, schedule their care tasks, and view everything
    in one convenient place.
    """
)

st.divider()

# -------------------------------
# PET MANAGEMENT
# -------------------------------

st.subheader("🐶 Manage Your Pets")

with st.form("add_pet_form"):

    pet_name = st.text_input("Pet Name")

    species = st.selectbox(
        "Species",
        ["Dog", "Cat", "Bird", "Rabbit", "Other"]
    )

    age = st.number_input(
        "Age",
        min_value=0,
        max_value=100,
        value=0
    )

    add_pet = st.form_submit_button("Add Pet")

    if add_pet:

        if pet_name.strip():

            new_pet = Pet(
                name=pet_name.strip(),
                species=species,
                age=age
            )

            st.session_state.owner.add_pet(new_pet)

            st.success(f"{pet_name} was added successfully!")

        else:
            st.warning("Please enter a pet name.")


st.markdown("### Registered Pets")

if st.session_state.owner.pets:

    for pet in st.session_state.owner.pets:
        st.write(f"🐾 {pet.name} ({pet.species}, Age {pet.age})")

else:
    st.info("No pets registered yet.")

st.divider()

# -------------------------------
# TASK MANAGEMENT
# -------------------------------

st.subheader("📋 Schedule Care Tasks")

pets = st.session_state.owner.pets

if pets:

    with st.form("add_task_form"):

        selected_pet_index = st.selectbox(
            "Select Pet",
            range(len(pets)),
            format_func=lambda i: pets[i].name
        )

        description = st.text_input("Task Description")

        task_date = st.date_input(
            "Due Date",
            value=date.today()
        )

        task_time = st.time_input("Scheduled Time")

        duration = st.number_input(
            "Duration (minutes)",
            min_value=1,
            value=15
        )

        priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High"]
        )

        frequency = st.selectbox(
            "Frequency",
            ["Once", "Daily", "Weekly"]
        )

        add_task = st.form_submit_button("Add Task")

        if add_task:

            if description.strip():

                new_task = Task(
                    description=description.strip(),
                    time=task_time.strftime("%H:%M"),
                    due_date=task_date,
                    duration=duration,
                    priority=priority,
                    frequency=frequency
                )

                selected_pet = pets[selected_pet_index]

                selected_pet.add_task(new_task)

                st.success(
                    f"Task '{description}' added for {selected_pet.name}!"
                )

            else:
                st.warning("Please enter a task description.")

else:
    st.info("Add a pet before scheduling tasks.")

st.divider()

# -------------------------------
# SCHEDULE VIEWER
# -------------------------------

st.subheader("📅 Pet Care Schedule")

scheduler = st.session_state.scheduler

# Keep the schedule visible after interacting with buttons
if "show_schedule" not in st.session_state:
    st.session_state.show_schedule = False

# -------------------------------
# FILTER CONTROLS
# -------------------------------

st.markdown("### 🔎 Filter Your Schedule")

col1, col2 = st.columns(2)

with col1:
    date_filter = st.selectbox(
        "Date",
        ["Today", "Tomorrow", "All Dates"]
    )

with col2:
    status_filter = st.selectbox(
        "Status",
        ["All", "Pending", "Completed"]
    )

pet_options = ["All Pets"] + [
    pet.name for pet in st.session_state.owner.pets
]

selected_pet = st.selectbox(
    "Pet",
    pet_options
)

if st.button("Generate Schedule"):
    st.session_state.show_schedule = True

# -------------------------------
# GENERATE FILTERED SCHEDULE
# -------------------------------

if st.session_state.show_schedule:

    # Convert selected filters into scheduler arguments
    pet_name = (
        None
        if selected_pet == "All Pets"
        else selected_pet
    )

    completed = None

    if status_filter == "Pending":
        completed = False
    elif status_filter == "Completed":
        completed = True

    # Retrieve filtered tasks
    schedule = scheduler.filter_tasks(
        pet_name=pet_name,
        completed=completed
    )

    # Apply date filtering
    from datetime import timedelta

    if date_filter == "Today":
        schedule = [
            task for task in schedule
            if task.due_date == date.today()
        ]

    elif date_filter == "Tomorrow":
        tomorrow = date.today() + timedelta(days=1)

        schedule = [
            task for task in schedule
            if task.due_date == tomorrow
        ]

    # -------------------------------
    # DISPLAY SCHEDULE
    # -------------------------------

    if schedule:

        schedule_data = []

        for task in schedule:

            # Identify the pet associated with the task
            pet_name = "Unknown"

            for pet in st.session_state.owner.pets:
                if any(existing_task is task for existing_task in pet.tasks):
                    pet_name = pet.name
                    break

            schedule_data.append({
                "Pet": pet_name,
                "Activity": task.description,
                "Date": str(task.due_date),
                "Time": task.time,
                "Duration": f"{task.duration} min",
                "Priority": task.priority,
                "Frequency": task.frequency,
                "Status": (
                    "Completed"
                    if task.completed
                    else "Pending"
                )
            })

        st.table(schedule_data)

        st.success(
            f"Schedule generated successfully! "
            f"{len(schedule)} task(s) found."
        )

        # -------------------------------
        # TASK COMPLETION
        # -------------------------------

        st.markdown("### ✅ Complete Tasks")

        for task in schedule:

            if not task.completed:

                col1, col2 = st.columns([3, 1])

                with col1:
                    st.write(
                        f"{task.description} — "
                        f"{task.due_date} at {task.time}"
                    )

                with col2:
                    if st.button(
                        "Mark Complete",
                        key=f"complete_{id(task)}"
                    ):
                        scheduler.mark_task_complete(task)
                        st.rerun()

        # -------------------------------
        # CONFLICT DETECTION
        # -------------------------------

        conflicts = scheduler.detect_conflicts()

        # Match conflict warnings to the selected date
        if date_filter == "Today":
            conflicts = [
                conflict for conflict in conflicts
                if str(date.today()) in conflict
            ]

        elif date_filter == "Tomorrow":
            tomorrow = date.today() + timedelta(days=1)

            conflicts = [
                conflict for conflict in conflicts
                if str(tomorrow) in conflict
            ]

        if conflicts:

            st.warning(
                f"⚠️ {len(conflicts)} scheduling conflict(s) detected!"
            )

            for conflict in conflicts:
                st.error(conflict)

        else:
            st.success("✅ No scheduling conflicts detected.")

    else:
        st.info("No tasks match the selected filters.")