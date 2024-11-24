#  KISA  EMMANUEL
#  KATENDE  DERRICK
#  EMURON  IAN


import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import heapq
import matplotlib.pyplot as plt

class Task:
    def __init__(self, task_id, description, deadline, priority, task_type, duration):
        self.task_id = task_id
        self.description = description
        self.deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M")
        self.priority = priority
        self.task_type = task_type  # 'personal' or 'academic'
        self.duration = duration  # in minutes
    
    def __lt__(self, other):
        return self.deadline < other.deadline

class Scheduler:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        heapq.heappush(self.tasks, task)
    
    def get_sorted_tasks(self, by="deadline"):
        if by == "deadline":
            return sorted(self.tasks, key=lambda x: x.deadline)
        elif by == "priority":
            return sorted(self.tasks, key=lambda x: x.priority, reverse=True)
        elif by == "type":
            return sorted(self.tasks, key=lambda x: x.task_type)

    def optimize_schedule(self, total_minutes):
        n = len(self.tasks)
        dp = [[0 for _ in range(total_minutes + 1)] for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            task = self.tasks[i - 1]
            for t in range(total_minutes + 1):
                if task.duration <= t:
                    dp[i][t] = max(dp[i - 1][t], dp[i - 1][t - task.duration] + task.priority)
                else:
                    dp[i][t] = dp[i - 1][t]
        
        t = total_minutes
        selected_tasks = []
        for i in range(n, 0, -1):
            if dp[i][t] != dp[i - 1][t]:
                selected_tasks.append(self.tasks[i - 1])
                t -= self.tasks[i - 1].duration
        return selected_tasks
    
    def plot_schedule(self):
        fig, ax = plt.subplots()
        start_time = datetime.now()
        for i, task in enumerate(self.tasks):
            start = (task.deadline - start_time).total_seconds() / 60
            ax.broken_barh([(start, task.duration)], (i * 10, 9), facecolors='tab:blue')
            ax.text(start, i * 10 + 5, f"{task.description}", va='center')
        
        plt.show()

scheduler = Scheduler()

class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Scheduling Assistant")
        
        # Frame for task entry
        self.entry_frame = tk.Frame(root)
        self.entry_frame.pack(pady=10)
        
        tk.Label(self.entry_frame, text="Task Description").grid(row=0, column=0)
        tk.Label(self.entry_frame, text="Deadline (YYYY-MM-DD HH:MM)").grid(row=0, column=1)
        tk.Label(self.entry_frame, text="Priority").grid(row=0, column=2)
        tk.Label(self.entry_frame, text="Task Type").grid(row=0, column=3)
        tk.Label(self.entry_frame, text="Duration (mins)").grid(row=0, column=4)
        
        self.desc_entry = tk.Entry(self.entry_frame)
        self.deadline_entry = tk.Entry(self.entry_frame)
        self.priority_entry = tk.Entry(self.entry_frame)
        self.type_entry = tk.Entry(self.entry_frame)
        self.duration_entry = tk.Entry(self.entry_frame)
        
        self.desc_entry.grid(row=1, column=0)
        self.deadline_entry.grid(row=1, column=1)
        self.priority_entry.grid(row=1, column=2)
        self.type_entry.grid(row=1, column=3)
        self.duration_entry.grid(row=1, column=4)
        
        tk.Button(self.entry_frame, text="Add Task", command=self.add_task).grid(row=1, column=5)
        
        # Frame for task display and optimization
        self.task_frame = tk.Frame(root)
        self.task_frame.pack(pady=10)
        
        self.tree = ttk.Treeview(self.task_frame, columns=("ID", "Description", "Deadline", "Priority", "Type", "Duration"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Deadline", text="Deadline")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Duration", text="Duration")
        
        self.tree.pack()
        
        tk.Button(root, text="Optimize Schedule", command=self.optimize_schedule).pack(pady=5)
        tk.Button(root, text="Show Gantt Chart", command=self.show_gantt_chart).pack(pady=5)

    def add_task(self):
        try:
            task_id = len(scheduler.tasks) + 1
            description = self.desc_entry.get()
            deadline = self.deadline_entry.get()
            priority = int(self.priority_entry.get())
            task_type = self.type_entry.get()
            duration = int(self.duration_entry.get())
            
            task = Task(task_id, description, deadline, priority, task_type, duration)
            scheduler.add_task(task)
            self.tree.insert("", "end", values=(task_id, description, deadline, priority, task_type, duration))
            
            # Clear entries
            self.desc_entry.delete(0, tk.END)
            self.deadline_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)
            self.type_entry.delete(0, tk.END)
            self.duration_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid task details.")
    
    def optimize_schedule(self):
        try:
            total_minutes = int(tk.simpledialog.askstring("Optimize Schedule", "Enter available time in minutes:"))
            optimized_tasks = scheduler.optimize_schedule(total_minutes)
            optimized_message = "\n".join([f"{task.description} (Priority: {task.priority})" for task in optimized_tasks])
            messagebox.showinfo("Optimized Tasks", f"Selected tasks for optimized schedule:\n\n{optimized_message}")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid time in minutes.")
    
    def show_gantt_chart(self):
        scheduler.plot_schedule()

# Run the application
root = tk.Tk()
app = SchedulerApp(root)
root.mainloop()

#                   
#                                  PSEUDO CODE

# Class Task:
#     Input: task_id, description, deadline, priority, task_type, duration
#     Initialize:
#         - Set task_id, description, deadline, priority, task_type, duration attributes
#         - Convert deadline from string to datetime object
#     Method: __lt__(self, other)
#         - Define comparison based on deadline for sorting in priority queue

# Class Scheduler:
#     Initialize:
#         - Create an empty list of tasks
    
#     Method: add_task(task)
#         - Add task to tasks list as a min-heap (sorted by deadline)

#     Method: view_tasks(by="deadline")
#         Input: sorting criterion (by: 'deadline', 'priority', 'type')
#         - Retrieve sorted tasks by calling get_sorted_tasks(by)
#         - For each task in sorted tasks:
#             - Print task_id, description, type, deadline, priority

#     Method: get_sorted_tasks(by="deadline")
#         Input: sorting criterion (by: 'deadline', 'priority', 'type')
#         Output: list of tasks sorted by criterion
#         - If criterion is 'deadline':
#             - Sort tasks by deadline in ascending order
#         - Else if criterion is 'priority':
#             - Sort tasks by priority in descending order
#         - Else if criterion is 'type':
#             - Sort tasks by task type (e.g., personal or academic)
#         - Return sorted list of tasks

#     Method: search_task_by_deadline(target_date)
#         Input: target_date (datetime object)
#         Output: list of tasks with deadlines on target_date
#         - Sort tasks by deadline
#         - Initialize binary search on sorted tasks:
#             - If middle task’s deadline date matches target_date:
#                 - Add task to results list
#                 - Check neighboring tasks (left and right) for matching dates and add them
#             - Else if middle task's deadline is earlier than target_date:
#                 - Move search to the right half
#             - Else:
#                 - Move search to the left half
#         - Return list of matching tasks

#     Method: optimize_schedule(total_minutes)
#         Input: total_minutes (available time in minutes)
#         Output: list of selected tasks that maximize priority within time limit
#         - Initialize 2D DP array (dp) with dimensions [num_tasks + 1][total_minutes + 1]
#         - For each task i from 1 to num_tasks:
#             - For each time t from 0 to total_minutes:
#                 - If task’s duration is <= t:
#                     - Set dp[i][t] to max(dp[i - 1][t], dp[i - 1][t - task.duration] + task.priority)
#                 - Else:
#                     - Set dp[i][t] to dp[i - 1][t]
#         - Trace back from dp array to find selected tasks:
#             - Starting from dp[num_tasks][total_minutes], identify tasks contributing to the solution
#         - Return list of selected tasks

#     Method: plot_schedule()
#         - Initialize a Gantt chart plot
#         - Define start time as the current time
#         - For each task in tasks list:
#             - Calculate start time offset as (task.deadline - start_time).minutes
#             - Add task to Gantt chart as a bar from start offset with width of task duration
#         - Display Gantt chart

# Creating Scheduler instance

# # Example: Adding Tasks
# Add Task(1, "Math homework", "2023-11-15 16:00", 10, "academic", 60) to Scheduler
# Add Task(2, "Doctor appointment", "2023-11-15 10:00", 8, "personal", 30) to Scheduler
# Add Task(3, "Group project", "2023-11-16 14:00", 9, "academic", 120) to Scheduler
# Add Task(4, "Exercise", "2023-11-15 18:00", 5, "personal", 45) to Scheduler

# # View Tasks Sorted by Deadline
# Call view_tasks(by="deadline")

# # Search for Tasks on Specific Date
# Call search_task_by_deadline(target_date="2023-11-15")

# # Optimize Schedule for Available Time
# Call optimize_schedule(total_minutes=180)

# # Plot Schedule with Gantt Chart
# Call plot_schedule()









