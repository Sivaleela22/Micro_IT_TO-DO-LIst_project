import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

TASKS_FILE = "tasks_gui.json"

# Load tasks from file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return []

# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

# Refresh task list display
def refresh_task_list():
    for widget in task_frame.winfo_children():
        widget.destroy()
    for i, task in enumerate(tasks):
        color = "green" if task["completed"] else "black"
        text = f"{i + 1}. {'[✓]' if task['completed'] else '[ ]'} {task['task']} | {task['category']} | {task['priority']}"
        label = tk.Label(task_frame, text=text, fg=color, anchor="w")
        label.pack(fill='x')
        label.bind("<Button-1>", lambda e, idx=i: on_task_click(idx))

# Handle task click
def on_task_click(index):
    selected_index.set(index)
    task = tasks[index]
    task_entry.delete(0, tk.END)
    task_entry.insert(0, task['task'])
    category_var.set(task['category'])
    priority_var.set(task['priority'])

# Add new task
def add_task():
    task_desc = task_entry.get().strip()
    category = category_var.get()
    priority = priority_var.get()
    if not task_desc:
        messagebox.showwarning("Input Error", "Task description cannot be empty.")
        return
    tasks.append({
        "task": task_desc,
        "completed": False,
        "category": category,
        "priority": priority
    })
    save_tasks(tasks)
    refresh_task_list()
    task_entry.delete(0, tk.END)

# Mark selected task as complete
def mark_complete():
    index = selected_index.get()
    if index is None:
        messagebox.showwarning("Selection Error", "Please select a task first.")
        return
    tasks[index]["completed"] = True
    save_tasks(tasks)
    refresh_task_list()

# Edit selected task
def edit_task():
    index = selected_index.get()
    if index is None:
        messagebox.showwarning("Selection Error", "Please select a task first.")
        return
    task_desc = task_entry.get().strip()
    category = category_var.get()
    priority = priority_var.get()
    if not task_desc:
        messagebox.showwarning("Input Error", "Task description cannot be empty.")
        return
    tasks[index]["task"] = task_desc
    tasks[index]["category"] = category
    tasks[index]["priority"] = priority
    save_tasks(tasks)
    refresh_task_list()
    selected_index.set(None)
    task_entry.delete(0, tk.END)

# Delete selected task
def delete_task():
    index = selected_index.get()
    if index is None:
        messagebox.showwarning("Selection Error", "Please select a task first.")
        return
    del tasks[index]
    save_tasks(tasks)
    refresh_task_list()
    selected_index.set(None)
    task_entry.delete(0, tk.END)

# Initialize GUI
root = tk.Tk()
root.title("📝 Advanced To-Do List")
root.geometry("500x500")

# Variables
selected_index = tk.IntVar(value=None)
categories = ["Work", "Personal", "Study", "Shopping", "Other"]
priorities = ["High", "Medium", "Low"]

# Input Fields
tk.Label(root, text="Task Description:").pack(pady=5)
task_entry = tk.Entry(root, width=50)
task_entry.pack()

tk.Label(root, text="Category:").pack(pady=5)
category_var = tk.StringVar(value=categories[0])
ttk.Combobox(root, textvariable=category_var, values=categories).pack()

tk.Label(root, text="Priority:").pack(pady=5)
priority_var = tk.StringVar(value=priorities[0])
ttk.Combobox(root, textvariable=priority_var, values=priorities).pack()

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Task", command=add_task, width=12).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Edit Selected", command=edit_task, width=12).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete Selected", command=delete_task, width=12).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Mark Complete", command=mark_complete, width=12).grid(row=0, column=3, padx=5)

# Task List Display
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
task_frame = tk.Frame(canvas)

task_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=task_frame, anchor="nw", width=480)
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Load and show tasks
tasks = load_tasks()
refresh_task_list()

# Run the app
root.mainloop()