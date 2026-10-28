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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
