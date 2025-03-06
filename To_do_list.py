import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import json
import os
from tkinter.font import Font


class ProfessionalToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskMaster Pro")
        self.root.geometry("800x700")
        self.root.minsize(650, 600)
        
        # Set the file path for saving/loading tasks
        self.tasks_file = "taskmaster_tasks.json"
        
        # Custom color scheme
        self.colors = {
            "primary": "#2E5090",
            "secondary": "#3A6BC5",
            "accent": "#4CAF50",
            "danger": "#D32F2F",
            "warning": "#FFC107",
            "background": "#F5F7FA",
            "card": "#FFFFFF",
            "text": "#333333",
            "text_secondary": "#757575",
            "completed": "#A5D6A7"
        }
        
        self.root.configure(bg=self.colors["background"])
        
        # Custom fonts
        self.title_font = Font(family="Helvetica", size=24, weight="bold")
        self.subtitle_font = Font(family="Helvetica", size=14)
        self.button_font = Font(family="Helvetica", size=11, weight="bold")
        self.text_font = Font(family="Helvetica", size=12)
        
        # Initialize task categories and priorities
        self.categories = ["Work", "Personal", "Shopping", "Health", "Other"]
        self.priorities = ["High", "Medium", "Low"]
        
        # Initialize tasks
        self.tasks = []
        
        # Create UI
        self.create_header()
        self.create_sidebar()
        self.create_task_input()
        self.create_task_list()
        self.create_footer()
        
        # Apply some padding to the entire UI
        for child in self.root.winfo_children():
            child.pack_configure(padx=10, pady=5)
            
        # Load tasks from file
        self.load_tasks_from_file()
        
        # Bind the window close event to save tasks
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            
    def create_header(self):
        """Create the application header with title and date"""
        header_frame = tk.Frame(self.root, bg=self.colors["primary"], height=80)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            header_frame, 
            text="TaskMaster Pro", 
            font=self.title_font, 
            bg=self.colors["primary"], 
            fg="white"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Current date display
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        date_label = tk.Label(
            header_frame, 
            text=current_date, 
            font=self.subtitle_font, 
            bg=self.colors["primary"], 
            fg="white"
        )
        date_label.pack(side=tk.RIGHT, padx=20, pady=20)
        
    def create_sidebar(self):
        """Create the sidebar with statistics and filters"""
        main_container = tk.Frame(self.root, bg=self.colors["background"])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        self.sidebar = tk.Frame(main_container, bg=self.colors["card"], width=200, relief=tk.RIDGE, bd=1)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Make sure sidebar maintains its width
        self.sidebar.pack_propagate(False)
        
        # Statistics header
        stats_label = tk.Label(
            self.sidebar, 
            text="Dashboard", 
            font=self.button_font, 
            bg=self.colors["card"], 
            fg=self.colors["primary"]
        )
        stats_label.pack(pady=(20, 10), anchor="w", padx=10)
        
        # Task stats (will be updated later)
        self.total_tasks_label = tk.Label(
            self.sidebar, 
            text="Total Tasks: 0", 
            font=self.text_font, 
            bg=self.colors["card"], 
            fg=self.colors["text"]
        )
        self.total_tasks_label.pack(pady=5, anchor="w", padx=10)
        
        self.completed_tasks_label = tk.Label(
            self.sidebar, 
            text="Completed: 0", 
            font=self.text_font, 
            bg=self.colors["card"], 
            fg=self.colors["text"]
        )
        self.completed_tasks_label.pack(pady=5, anchor="w", padx=10)
        
        # Filter section
        filter_label = tk.Label(
            self.sidebar, 
            text="Filter Tasks", 
            font=self.button_font, 
            bg=self.colors["card"], 
            fg=self.colors["primary"]
        )
        filter_label.pack(pady=(20, 10), anchor="w", padx=10)
        
        # Filter buttons
        filter_all = tk.Button(
            self.sidebar, 
            text="All Tasks", 
            bg=self.colors["secondary"], 
            fg="white", 
            font=self.button_font, 
            relief=tk.FLAT, 
            command=lambda: self.filter_tasks("all"),
            width=15
        )
        filter_all.pack(pady=5)
        
        filter_active = tk.Button(
            self.sidebar, 
            text="Active", 
            bg=self.colors["card"], 
            fg=self.colors["text"], 
            font=self.button_font, 
            relief=tk.FLAT, 
            command=lambda: self.filter_tasks("active"),
            width=15
        )
        filter_active.pack(pady=5)
        
        filter_completed = tk.Button(
            self.sidebar, 
            text="Completed", 
            bg=self.colors["card"], 
            fg=self.colors["text"], 
            font=self.button_font, 
            relief=tk.FLAT, 
            command=lambda: self.filter_tasks("completed"),
            width=15
        )
        filter_completed.pack(pady=5)
        
        # Content container (main area)
        self.content_container = tk.Frame(main_container, bg=self.colors["background"])
        self.content_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_task_input(self):
        """Create the task input area with additional fields"""
        input_frame = tk.Frame(self.content_container, bg=self.colors["card"], relief=tk.RIDGE, bd=1)
        input_frame.pack(fill=tk.X, pady=10)
        
        # Title for input section
        input_title = tk.Label(
            input_frame, 
            text="Add New Task", 
            font=self.button_font, 
            bg=self.colors["card"], 
            fg=self.colors["primary"]
        )
        input_title.grid(row=0, column=0, columnspan=3, sticky="w", padx=15, pady=(15, 5))
        
        # Task name input
        task_label = tk.Label(
            input_frame, 
            text="Task:", 
            font=self.text_font, 
            bg=self.colors["card"], 
            fg=self.colors["text"]
        )
        task_label.grid(row=1, column=0, sticky="w", padx=15, pady=5)
        
        self.task_entry = tk.Entry(
            input_frame, 
            width=40, 
            font=self.text_font, 
            relief=tk.SOLID, 
            bd=1
        )
        self.task_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # Category dropdown
        category_label = tk.Label(
            input_frame, 
            text="Category:", 
            font=self.text_font, 
            bg=self.colors["card"], 
            fg=self.colors["text"]
        )
        category_label.grid(row=2, column=0, sticky="w", padx=15, pady=5)
        
        self.category_var = tk.StringVar()
        self.category_var.set(self.categories[0])
        category_dropdown = ttk.Combobox(
            input_frame, 
            textvariable=self.category_var, 
            values=self.categories, 
            state="readonly", 
            font=self.text_font, 
            width=15
        )
        category_dropdown.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # Priority dropdown
        priority_label = tk.Label(
            input_frame, 
            text="Priority:", 
            font=self.text_font, 
            bg=self.colors["card"], 
            fg=self.colors["text"]
        )
        priority_label.grid(row=2, column=1, sticky="e", padx=(150, 5), pady=5)
        
        self.priority_var = tk.StringVar()
        self.priority_var.set(self.priorities[1])  # Default: Medium
        priority_dropdown = ttk.Combobox(
            input_frame, 
            textvariable=self.priority_var, 
            values=self.priorities, 
            state="readonly", 
            font=self.text_font, 
            width=10
        )
        priority_dropdown.grid(row=2, column=2, sticky="w", padx=5, pady=5)
        
        # Due date
        date_label = tk.Label(
            input_frame, 
            text="Due Date:", 
            font=self.text_font, 
            bg=self.colors["card"], 
            fg=self.colors["text"]
        )
        date_label.grid(row=3, column=0, sticky="w", padx=15, pady=5)
        
        self.due_date_entry = tk.Entry(
            input_frame, 
            width=15, 
            font=self.text_font
        )
        self.due_date_entry.insert(0, "MM/DD/YYYY")
        self.due_date_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        # Add button
        add_button = tk.Button(
            input_frame, 
            text="Add Task", 
            command=self.add_task, 
            bg=self.colors["accent"], 
            fg="white", 
            font=self.button_font, 
            padx=15, 
            pady=5, 
            relief=tk.FLAT
        )
        add_button.grid(row=3, column=2, padx=15, pady=15, sticky="e")
        
        # Configure grid to expand properly
        input_frame.grid_columnconfigure(1, weight=1)
        
    def create_task_list(self):
        """Create the task list area with enhanced styling"""
        list_frame = tk.Frame(self.content_container, bg=self.colors["card"], relief=tk.RIDGE, bd=1)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Title for task list
        list_title = tk.Label(
            list_frame, 
            text="Your Tasks", 
            font=self.button_font, 
            bg=self.colors["card"], 
            fg=self.colors["primary"]
        )
        list_title.pack(anchor="w", padx=15, pady=(15, 5))
        
        # Create columns for task list
        columns = ("task", "category", "priority", "due_date", "status")
        self.task_tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
        
        # Configure column headings
        self.task_tree.heading("task", text="Task")
        self.task_tree.heading("category", text="Category")
        self.task_tree.heading("priority", text="Priority")
        self.task_tree.heading("due_date", text="Due Date")
        self.task_tree.heading("status", text="Status")
        
        # Configure column widths
        self.task_tree.column("task", width=250, minwidth=200)
        self.task_tree.column("category", width=100, minwidth=80)
        self.task_tree.column("priority", width=80, minwidth=80)
        self.task_tree.column("due_date", width=100, minwidth=80)
        self.task_tree.column("status", width=80, minwidth=80)
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscroll=scrollbar.set)
        
        # Pack tree and scrollbar
        self.task_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 15), pady=10)
        
        # Bind double click to mark task as done
        self.task_tree.bind("<Double-1>", self.toggle_task_status)
        
    def create_footer(self):
        """Create footer with action buttons"""
        footer_frame = tk.Frame(self.content_container, bg=self.colors["background"])
        footer_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Action buttons
        self.mark_done_button = tk.Button(
            footer_frame, 
            text="Mark as Done", 
            command=self.mark_as_done, 
            bg=self.colors["accent"], 
            fg="white", 
            font=self.button_font, 
            padx=15, 
            pady=8, 
            relief=tk.FLAT
        )
        self.mark_done_button.pack(side=tk.LEFT, padx=5)
        
        self.remove_button = tk.Button(
            footer_frame, 
            text="Remove Task", 
            command=self.remove_task, 
            bg=self.colors["danger"], 
            fg="white", 
            font=self.button_font, 
            padx=15, 
            pady=8, 
            relief=tk.FLAT
        )
        self.remove_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = tk.Button(
            footer_frame, 
            text="Clear All", 
            command=self.clear_all, 
            bg=self.colors["warning"], 
            fg="white", 
            font=self.button_font, 
            padx=15, 
            pady=8, 
            relief=tk.FLAT
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Add Save button
        self.save_button = tk.Button(
            footer_frame, 
            text="Save Tasks", 
            command=self.save_tasks_to_file, 
            bg=self.colors["secondary"], 
            fg="white", 
            font=self.button_font, 
            padx=15, 
            pady=8, 
            relief=tk.FLAT
        )
        self.save_button.pack(side=tk.RIGHT, padx=5)
        
    def add_task(self):
        """Adds a new task to the list with category, priority and due date"""
        task = self.task_entry.get().strip()
        category = self.category_var.get()
        priority = self.priority_var.get()
        due_date = self.due_date_entry.get()
        
        # Validate inputs
        if not task:
            messagebox.showwarning("Warning", "Task cannot be empty!")
            return
            
        # Create task item
        task_id = len(self.tasks)
        task_item = {
            "id": task_id,
            "task": task,
            "category": category,
            "priority": priority,
            "due_date": due_date,
            "status": "Pending"
        }
        
        # Add to tasks list
        self.tasks.append(task_item)
        
        # Add to treeview
        item_id = self.task_tree.insert("", tk.END, values=(
            task, category, priority, due_date, "Pending"
        ))
        
        # Set row color based on priority
        if priority == "High":
            self.task_tree.tag_configure(f"priority_{task_id}", background="#FFEBEE")
            self.task_tree.item(item_id, tags=(f"priority_{task_id}",))
        elif priority == "Medium":
            self.task_tree.tag_configure(f"priority_{task_id}", background="#FFF8E1")
            self.task_tree.item(item_id, tags=(f"priority_{task_id}",))
        
        # Clear entry fields
        self.task_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
        self.due_date_entry.insert(0, "MM/DD/YYYY")
        
        # Update stats
        self.update_stats()
        
        # Save tasks to file
        self.save_tasks_to_file()
        
    def remove_task(self):
        """Removes the selected task"""
        try:
            selected_item = self.task_tree.selection()[0]
            # Get index of the task
            item_values = self.task_tree.item(selected_item, "values")
            task_name = item_values[0]
            
            # Remove from tasks list
            for i, task in enumerate(self.tasks):
                if task["task"] == task_name:
                    self.tasks.pop(i)
                    break
            
            # Remove from treeview
            self.task_tree.delete(selected_item)
            
            # Update stats
            self.update_stats()
   
            # Save tasks to file
            self.save_tasks_to_file()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to remove!")
        
    def mark_as_done(self):
        """Marks a selected task as completed or pending"""
        try:
            selected_item = self.task_tree.selection()[0]
            item_values = self.task_tree.item(selected_item, "values")
            
            # Get current status and toggle it
            current_status = item_values[4]
            new_status = "Completed" if current_status == "Pending" else "Pending"
            
            # Update treeview
            self.task_tree.item(selected_item, values=(
                item_values[0], item_values[1], item_values[2], item_values[3], new_status
            ))
            
            # Update task list
            task_name = item_values[0]
            for task in self.tasks:
                if task["task"] == task_name:
                    task["status"] = new_status
                    break
                    
            # Update row color
            if new_status == "Completed":
                self.task_tree.tag_configure(f"completed_{task_name}", background=self.colors["completed"])
                self.task_tree.item(selected_item, tags=(f"completed_{task_name}",))
            else:
                # Remove completed tag
                self.task_tree.item(selected_item, tags=())
                
                # Re-apply priority tag if needed
                for task in self.tasks:
                    if task["task"] == task_name:
                        if task["priority"] == "High":
                            self.task_tree.tag_configure(f"priority_{task['id']}", background="#FFEBEE")
                            self.task_tree.item(selected_item, tags=(f"priority_{task['id']}",))
                        elif task["priority"] == "Medium":
                            self.task_tree.tag_configure(f"priority_{task['id']}", background="#FFF8E1")
                            self.task_tree.item(selected_item, tags=(f"priority_{task['id']}",))
                        break
            
            # Update stats
            self.update_stats()
 
            # Save tasks to file
            self.save_tasks_to_file()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to mark as done!")
    
    def toggle_task_status(self, event):
        """Toggle task status on double click"""
        self.mark_as_done()
        
    def clear_all(self):
        """Clears all tasks from the list"""
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?")
        if confirm:
            # Clear treeview
            for item in self.task_tree.get_children():
                self.task_tree.delete(item)
            
            # Clear tasks list
            self.tasks.clear()
            
            # Update stats
            self.update_stats() 
            # Save tasks to file (which will be empty)
            self.save_tasks_to_file()
    
    def filter_tasks(self, filter_type):
        """Filter tasks based on status"""
        # Clear current view
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Apply filter
        for task in self.tasks:
            if filter_type == "all" or \
               (filter_type == "active" and task["status"] == "Pending") or \
               (filter_type == "completed" and task["status"] == "Completed"):
                
                item_id = self.task_tree.insert("", tk.END, values=(
                    task["task"], task["category"], task["priority"], 
                    task["due_date"], task["status"]
                ))
                
                # Apply styling
                if task["status"] == "Completed":
                    self.task_tree.tag_configure(f"completed_{task['task']}", background=self.colors["completed"])
                    self.task_tree.item(item_id, tags=(f"completed_{task['task']}",))
                elif task["priority"] == "High":
                    self.task_tree.tag_configure(f"priority_{task['id']}", background="#FFEBEE")
                    self.task_tree.item(item_id, tags=(f"priority_{task['id']}",))
                elif task["priority"] == "Medium":
                    self.task_tree.tag_configure(f"priority_{task['id']}", background="#FFF8E1")
                    self.task_tree.item(item_id, tags=(f"priority_{task['id']}",))
    
    def update_stats(self):
        """Update statistics in sidebar"""
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for task in self.tasks if task["status"] == "Completed")
        
        self.total_tasks_label.config(text=f"Total Tasks: {total_tasks}")
        self.completed_tasks_label.config(text=f"Completed: {completed_tasks}")

    def save_tasks_to_file(self):
        """Save tasks to a JSON file"""
        try:
            with open(self.tasks_file, 'w') as file:
                json.dump(self.tasks, file)
                
            # Optional: Show a brief status message
            status_label = tk.Label(
                self.root, 
                text="Tasks saved successfully!", 
                bg=self.colors["accent"],
                fg="white",
                font=self.button_font,
                padx=10,
                pady=5
            )
            status_label.place(relx=0.5, rely=0.9, anchor="center")
            # Remove the message after 2 seconds
            self.root.after(2000, status_label.destroy)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {str(e)}")
    
    def load_tasks_from_file(self):
        """Load tasks from a JSON file"""
        try:
            if os.path.exists(self.tasks_file):
                with open(self.tasks_file, 'r') as file:
                    self.tasks = json.load(file)
                    
                # Clear existing items in treeview
                for item in self.task_tree.get_children():
                    self.task_tree.delete(item)
                    
                # Add tasks to treeview
                for task in self.tasks:
                    item_id = self.task_tree.insert("", tk.END, values=(
                        task["task"], task["category"], task["priority"], 
                        task["due_date"], task["status"]
                    ))
                    
                    # Apply styling
                    if task["status"] == "Completed":
                        self.task_tree.tag_configure(f"completed_{task['task']}", background=self.colors["completed"])
                        self.task_tree.item(item_id, tags=(f"completed_{task['task']}",))
                    elif task["priority"] == "High":
                        self.task_tree.tag_configure(f"priority_{task['id']}", background="#FFEBEE")
                        self.task_tree.item(item_id, tags=(f"priority_{task['id']}",))
                    elif task["priority"] == "Medium":
                        self.task_tree.tag_configure(f"priority_{task['id']}", background="#FFF8E1")
                        self.task_tree.item(item_id, tags=(f"priority_{task['id']}",))
                
                # Update stats
                self.update_stats()
                
                # Show a brief status message
                if self.tasks:
                    status_label = tk.Label(
                        self.root, 
                        text=f"Loaded {len(self.tasks)} tasks from file", 
                        bg=self.colors["secondary"],
                        fg="white",
                        font=self.button_font,
                        padx=10,
                        pady=5
                    )
                    status_label.place(relx=0.5, rely=0.9, anchor="center")
                    # Remove the message after 2 seconds
                    self.root.after(2000, status_label.destroy)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tasks: {str(e)}")
    
    def on_closing(self):
        """Handle window closing event"""
        # Save tasks before closing
        self.save_tasks_to_file()
        # Destroy the window
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ProfessionalToDoApp(root)
    root.mainloop()