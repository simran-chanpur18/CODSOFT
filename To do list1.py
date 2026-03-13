import json
import os
import random
from datetime import datetime, timedelta

TASKS_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE) as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def next_id(tasks):
    return max([t["id"] for t in tasks], default=0) + 1

def parse_date(text):
    """Convert 'today', 'tomorrow', or 'YYYY-MM-DD' to date string."""
    text = text.strip().lower()
    today = datetime.today().date()
    if text == "today":
        return today.isoformat()
    if text == "tomorrow":
        return (today + timedelta(days=1)).isoformat()
    try:
        datetime.strptime(text, "%Y-%m-%d")
        return text
    except ValueError:
        return None

def add_task(tasks):
    title = input("Task title: ").strip()
    if not title:
        print("ERROR: Title cannot be empty.")
        return
    due_input = input("Due date (today/tomorrow/YYYY-MM-DD, or leave blank): ").strip()
    due = parse_date(due_input) if due_input else None
    if due_input and not due:
        print("WARNING: Invalid date format. No due date set.")
    tasks.append({
        "id": next_id(tasks),
        "title": title,
        "due": due,
        "done": False
    })
    save_tasks(tasks)
    print(f"SUCCESS: Task added: {title}")

def list_tasks(tasks):
    if not tasks:
        print("Your to-do list is empty.")
        return
    print("\n" + "="*60)
    print("YOUR TASKS")
    print("="*60)
    today = datetime.today().date()
    for t in tasks:
        # Status symbol
        status = "[DONE]" if t["done"] else "[PENDING]"
        # Due date display
        if t["due"]:
            due_date = datetime.strptime(t["due"], "%Y-%m-%d").date()
            delta = (due_date - today).days
            if delta < 0:
                due_str = f"OVERDUE ({-delta} days ago)"
            elif delta == 0:
                due_str = "DUE TODAY"
            elif delta == 1:
                due_str = "Due tomorrow"
            else:
                due_str = f"Due in {delta} days"
        else:
            due_str = "No due date"
        print(f"{status} [ID {t['id']}] {t['title']} -- {due_str}")
    print("="*60 + "\n")

def mark_done(tasks):
    list_tasks(tasks)
    try:
        tid = int(input("Enter ID of completed task: "))
    except ValueError:
        print("ERROR: Invalid ID.")
        return
    for t in tasks:
        if t["id"] == tid:
            if t["done"]:
                print("WARNING: Task already done.")
            else:
                t["done"] = True
                save_tasks(tasks)
                print(f"Great job! '{t['title']}' completed!")
            return
    print("ERROR: Task not found.")

def delete_task(tasks):
    list_tasks(tasks)
    try:
        tid = int(input("Enter ID of task to delete: "))
    except ValueError:
        print("ERROR: Invalid ID.")
        return
    for i, t in enumerate(tasks):
        if t["id"] == tid:
            del tasks[i]
            save_tasks(tasks)
            print(f"Deleted: '{t['title']}'")
            return
    print("ERROR: Task not found.")

def show_stats(tasks):
    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    pending = total - done
    today = datetime.today().date()
    overdue = sum(1 for t in tasks if not t["done"] and t["due"] and
                  datetime.strptime(t["due"], "%Y-%m-%d").date() < today)
    print("\n" + "-"*30)
    print("STATISTICS")
    print("-"*30)
    print(f"Total tasks: {total}")
    print(f"Completed: {done}")
    print(f"Pending: {pending}")
    print(f"Overdue: {overdue}")
    if total:
        print(f"Completion rate: {done/total*100:.1f}%")
    print("-"*30)

def suggest_task():
    ideas = [
        "Write a thank‑you note",
        "Clean out your email inbox",
        "Try a new recipe",
        "Call a family member",
        "Plan your next weekend",
        "Organize one drawer",
        "Read for 20 minutes",
        "Drink a glass of water"
    ]
    print(f"\nSUGGESTION: {random.choice(ideas)}\n")

def main():
    print("="*60)
    print("              TO-DO LIST with DUE DATES")
    print("="*60)
    tasks = load_tasks()
    while True:
        print("\nOptions:")
        print("1. Add task")
        print("2. List tasks")
        print("3. Mark task as done")
        print("4. Delete task")
        print("5. Show statistics")
        print("6. Suggest a task idea")
        print("7. Exit")
        choice = input("Choose (1-7): ").strip()
        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            list_tasks(tasks)
        elif choice == "3":
            mark_done(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            show_stats(tasks)
        elif choice == "6":
            suggest_task()
        elif choice == "7":
            print("Goodbye! Keep crushing your goals.")
            break
        else:
            print("ERROR: Invalid choice.")

if __name__ == "__main__":
    main()
