import anthropic
from dotenv import load_dotenv
load_dotenv()
# Smart Task Manager
# Module 2 Practice Exercise

task_list = [
    {"description": "Reply to emails", "time_to_complete": 3, "priority": "high"},
    {"description": "Prepare sales presentation", "time_to_complete": 45, "priority": "high"},
    {"description": "Read AI newsletter", "time_to_complete": 10, "priority": "low"},
    {"description": "Update CRM notes", "time_to_complete": 5, "priority": "high"},
    {"description": "Watch Python tutorial", "time_to_complete": 30, "priority": "low"},
]
# Print every task description
print("=== ALL TASKS ===")
for task in task_list:
    print(task["description"])

    # Print only tasks that take less than 10 minutes
print("\n=== QUICK TASKS (under 10 mins) ===")
for task in task_list:
    if task["time_to_complete"] < 10:
        print(f"{task['description']} - {task['time_to_complete']} mins")
# Print only high priority tasks
print("\n=== HIGH PRIORITY ===")
for task in task_list:
    if task["priority"] == "high":
        print(task["description"])
        # Task 5 - Ask Claude to help prioritise your tasks
print("\n=== CLAUDE'S RECOMMENDATION ===")

# Build a list of all tasks as text
task_summary = ""
for task in task_list:
    task_summary += f"- {task['description']} ({task['time_to_complete']} mins, {task['priority']} priority)\n"

# Send to Claude
client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=256,
    messages=[{
        "role": "user",
        "content": f"""I have the following tasks to complete today:

{task_summary}

In 3 bullet points, tell me which order I should do these in and why."""
    }]
)

print(message.content[0].text)
