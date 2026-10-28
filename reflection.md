# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

For my initial PawPal+ design, I created a UML class diagram containing four main classes: Owner, Pet, Task, and Scheduler. I wanted to keep the architecture simple and modular so that each class would have a specific responsibility.

The Owner class manages the user’s pets and provides access to their tasks. The Pet class stores information about each pet, including its name, species, age, and scheduled activities. The Task class represents individual care activities, such as feeding, walking, and administering medication. It stores information such as the scheduled time, duration, priority, frequency, and completion status. Finally, the Scheduler class is responsible for organizing tasks, sorting them by time, filtering them, detecting scheduling conflicts, and managing recurring activities.

I designed the relationships so that one Owner can have multiple Pets, each Pet can have multiple Tasks, and the Scheduler can retrieve tasks through the Owner. I also chose to use Python dataclasses for the main data objects to reduce repetitive code and make the system easier to maintain.

Overall, my goal was to create a design that separates pet management from scheduling logic while allowing the different classes to work together.

**b. Design changes**

After reviewing my initial class skeletons with AI, I identified a few areas that could be improved during implementation. One concern was that tasks did not have unique identifiers, which could make it difficult to distinguish between activities with similar descriptions and scheduled times. Another concern was that the system did not yet validate scheduling information, meaning users could potentially enter invalid times or recurrence values.

I also reviewed how recurring tasks would be handled. I decided that the Task class should be responsible for calculating the next occurrence, while the Scheduler should manage creating the new task after the original is completed. This separation helps prevent duplicate logic and keeps each class focused on its responsibilities.

I decided to keep my original four-class architecture because the relationships and responsibilities were already appropriate for the project. Rather than adding unnecessary complexity to the initial design, I plan to address these improvements as I implement and test the application.

---
### Core User Actions

The three core actions I identified for PawPal+ are:

1. **Manage Pets:** Users should be able to add and manage multiple
   pets, including basic information such as their names and species.

2. **Schedule Care Tasks:** Users should be able to create tasks for
   their pets, including feeding, walking, medications, and appointments.
   Each task should include a scheduled time, duration, priority,
   and frequency.

3. **View and Manage Schedules:** Users should be able to view their
   pets' daily tasks in chronological order, identify scheduling
   conflicts, and mark tasks as completed.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler primarily considers the due date, scheduled time, duration, completion status, and recurrence frequency of each task. I implemented chronological sorting so activities are organized by their scheduled dates and times. The scheduler also uses task duration to identify overlapping activities and allows tasks to be filtered by pet or completion status.

I decided that time was the most important constraint because pet care activities often need to happen at specific times. For example, feeding and medication may need to follow a consistent schedule. Although the system stores priority levels for each task, I chose to organize activities chronologically rather than automatically rearranging them based on priority. This keeps the schedule predictable while still allowing users to identify which activities are more important.

**b. Tradeoffs**

One tradeoff I made was implementing conflict detection without automatic conflict resolution. My scheduler can identify when two activities overlap, but it does not automatically change their scheduled times.

I think this is reasonable because pet owners may have specific preferences or responsibilities that the application cannot fully understand. For example, a medication task might need to happen at a particular time, while a walk could be more flexible. Automatically rescheduling activities could create problems if the system moves something that should remain fixed.

By identifying conflicts and leaving the final decision to the user, the scheduler provides useful information without making potentially inappropriate scheduling decisions. This also keeps the implementation simpler and easier to test.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

I used pytest to test the main functionality of PawPal+, including task creation, task completion, chronological sorting, filtering, recurring tasks, and conflict detection. I wanted to make sure that the scheduler could correctly organize activities by date and time, filter tasks based on the pet or completion status, and generate new occurrences for daily and weekly tasks.

I also tested several edge cases, including empty schedules, duplicate task completion, and conflicts involving completed tasks. These tests were important because they helped me identify potential problems that might not be obvious during normal use. For example, completing the same recurring task twice should not create duplicate activities, and tasks scheduled back-to-back should not be considered conflicting.

All 12 automated tests passed successfully, which confirmed that the backend functionality behaved as expected in the scenarios I tested.

**b. Confidence**

I would rate my confidence in the scheduler as a 9 out of 10. The automated tests covered the main scheduling features, and all 12 tests passed without errors. I also manually tested the application during development, which helped me verify that the different components worked together.

However, I know that passing tests does not necessarily mean the application is completely free of bugs. If I had more time, I would test additional edge cases, such as tasks with invalid time formats, negative durations, and overlapping activities scheduled across midnight. I would also test how the scheduler handles a much larger number of pets and tasks to see whether performance becomes an issue.

Overall, this exercise strengthened my understanding of automated testing and why verification is important in software development. I learned that testing should cover both expected behavior and unusual situations to make sure an application is reliable.

---

## 5. Reflection

**a. What went well**

The part of this project I am most satisfied with is how the different components of PawPal+ came together to create a functional application. I started by designing the classes and their relationships, then gradually implemented the scheduling algorithms and connected them to the Streamlit interface. I particularly liked seeing the conflict detection and task completion features work in the actual application because they demonstrated how the backend logic could be used to solve practical problems.

I am also satisfied with the testing process. I created 12 automated tests covering the main functionality and several edge cases, and all of them passed. Building the application in phases made it easier to identify problems, verify individual features, and make improvements without having to redesign the entire system.

**b. What you would improve**

If I had another iteration, I would improve how recurring tasks are generated. Currently, PawPal+ creates the next occurrence of a daily or weekly task only after the previous occurrence is completed. Although this works, it limits how far ahead users can view their schedules. I would redesign this functionality so recurring tasks are generated automatically based on their frequency, regardless of whether earlier activities have been completed.

I would also add persistent data storage so pets and tasks remain available after the application is closed. Another improvement would be allowing users to edit or delete existing tasks directly from the Streamlit interface. These changes would make PawPal+ more practical for everyday use.

**c. Key takeaway**

One important thing I learned from this project is how much easier software development becomes when a system is divided into smaller components with clearly defined responsibilities. Designing the UML diagram before implementing the application helped me understand how the Owner, Pet, Task, and Scheduler classes should interact. It also made it easier to reuse existing methods when connecting the scheduling logic to Streamlit.

I also learned that AI can be a useful development partner, but its suggestions still need to be reviewed and tested. Throughout the project, I used AI to help organize the implementation, understand the code, and troubleshoot issues. However, I still needed to run the application, verify the results, and identify limitations that were not immediately obvious. This reinforced the importance of treating AI-generated code as something that needs to be evaluated rather than automatically assuming it is correct.
