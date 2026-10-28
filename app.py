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
# DAILY SCHEDULE
# -------------------------------

st.subheader("📅 Today's Schedule")

scheduler = st.session_state.scheduler

if st.button("Generate Schedule"):

    schedule = [
        task
        for task in scheduler.get_schedule()
        if task.due_date == date.today()
    ]

    if schedule:

        schedule_data = []

        for pet in st.session_state.owner.pets:

            for task in pet.tasks:

                if task.due_date == date.today():

                    schedule_data.append({
                        "Pet": pet.name,
                        "Activity": task.description,
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
            f"{len(schedule)} tasks scheduled for today."
        )

    else:
        st.info("No tasks scheduled for today.")