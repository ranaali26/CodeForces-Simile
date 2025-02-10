import tkinter as tk
from tkinter import ttk, messagebox
from utils.api_functions import user_status, accepted_submissions
from utils.statistics_functions import get_problem_statistics, sort_rating


class CodeforceComparator(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Codeforces Comparator")
        self.geometry("800x600")

        # Create main frame
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # User input section
        self.create_input_section()

        # Buttons section
        self.create_buttons_section()

        # Results section
        self.create_results_section()

    def create_input_section(self):
        # User handles input
        ttk.Label(self.main_frame, text="Your Handle:").grid(row=0, column=0, pady=5)
        self.user_handle = ttk.Entry(self.main_frame)
        self.user_handle.grid(row=0, column=1, pady=5)

        ttk.Label(self.main_frame, text="Friend's Handle:").grid(row=1, column=0, pady=5)
        self.friend_handle = ttk.Entry(self.main_frame)
        self.friend_handle.grid(row=1, column=1, pady=5)

        # Fetch button
        ttk.Button(self.main_frame, text="Fetch Data",
                   command=self.fetch_data).grid(row=2, column=0, columnspan=2, pady=10)

    def create_buttons_section(self):
        buttons_frame = ttk.LabelFrame(self.main_frame, text="Options", padding="10")
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        button_texts = [
            "Problems solved by friend only",
            "Problems solved by you only",
            "Your Statistics",
            "Friend's Statistics",
            "Compare Statistics"
        ]

        for idx, text in enumerate(button_texts):
            ttk.Button(buttons_frame, text=text,
                       command=lambda x=idx: self.handle_button_click(x)).pack(fill="x", pady=2)

    def create_results_section(self):
        # Results display
        results_frame = ttk.LabelFrame(self.main_frame, text="Results", padding="10")
        results_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")

        self.results_text = tk.Text(results_frame, height=15, width=60)
        self.results_text.pack(fill="both", expand=True)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.results_text.configure(yscrollcommand=scrollbar.set)

    def fetch_data(self):
        try:
            user = self.user_handle.get()
            friend = self.friend_handle.get()

            if not user or not friend:
                messagebox.showerror("Error", "Please enter both handles!")
                return

            # Using imported functions
            self.user_submissions = user_status(user)
            self.friend_submissions = user_status(friend)

            if self.user_submissions and self.friend_submissions:
                self.user_accepted = accepted_submissions(self.user_submissions)
                self.friend_accepted = accepted_submissions(self.friend_submissions)
                self.user_stats = get_problem_statistics(self.user_submissions)
                self.friend_stats = get_problem_statistics(self.friend_submissions)
                messagebox.showinfo("Success", "Data fetched successfully!")
            else:
                messagebox.showerror("Error", "Failed to fetch data!")

        except Exception as e:
            messagebox.showerror("Error", f"Error fetching data: {str(e)}")

    def handle_button_click(self, button_index):
        if not hasattr(self, 'user_submissions'):
            messagebox.showerror("Error", "Please fetch data first!")
            return

        self.results_text.delete(1.0, tk.END)

        if button_index == 0:  # Problems solved by friend only
            comparison = self.friend_accepted - self.user_accepted
            self.display_comparison(comparison, "Problems solved by friend but not by you")
        elif button_index == 1:  # Problems solved by you only
            comparison = self.user_accepted - self.friend_accepted
            self.display_comparison(comparison, "Problems solved by you but not by friend")
        elif button_index == 2:  # Your Statistics
            self.display_statistics(self.user_stats, self.user_handle.get())
        elif button_index == 3:  # Friend's Statistics
            self.display_statistics(self.friend_stats, self.friend_handle.get())
        elif button_index == 4:  # Compare Statistics
            self.compare_statistics()

    def display_comparison(self, comparison, title):
        self.results_text.insert(tk.END, f"{title}:\n\n")
        if not comparison:
            self.results_text.insert(tk.END, "No problems found!")
        else:
            sorted_comparison = sorted(comparison, key=sort_rating, reverse=True)
            for problem in sorted_comparison:
                self.results_text.insert(tk.END, f"{problem}\n")

    def display_statistics(self, stats, handle):
        self.results_text.insert(tk.END, f"Statistics for {handle}:\n\n")
        self.results_text.insert(tk.END, f"Total Submissions: {stats['total_submissions']}\n")
        self.results_text.insert(tk.END, f"Accepted Submissions: {stats['accepted_submissions']}\n")
        self.results_text.insert(tk.END, f"Unique Accepted Problems: {stats['unique_accepted_problems']}\n")
        self.results_text.insert(tk.END, f"Average Time to Solve: {stats['average_time_to_solve']:.2f} seconds\n\n")
        self.results_text.insert(tk.END, "Problem Ratings Distribution:\n")
        for rating, count in sorted(stats['problem_ratings'].items()):
            self.results_text.insert(tk.END, f"Rating {rating}: {count} problems\n")

    def compare_statistics(self):
        self.results_text.insert(tk.END, "Comparison of Statistics:\n\n")
        self.results_text.insert(tk.END,
                                 f"{'Metric':<25} {self.user_handle.get():<15} {self.friend_handle.get():<15}\n")
        self.results_text.insert(tk.END, "-" * 55 + "\n")

        metrics = [
            ('Total Submissions', 'total_submissions'),
            ('Accepted Submissions', 'accepted_submissions'),
            ('Unique Accepted Problems', 'unique_accepted_problems'),
            ('Average Time to Solve', 'average_time_to_solve')
        ]

        for metric_name, metric_key in metrics:
            user_value = self.user_stats[metric_key]
            friend_value = self.friend_stats[metric_key]
            if metric_key == 'average_time_to_solve':
                self.results_text.insert(tk.END,
                                         f"{metric_name:<25} {user_value:15.2f} {friend_value:15.2f}\n")
            else:
                self.results_text.insert(tk.END,
                                         f"{metric_name:<25} {user_value:<15} {friend_value:<15}\n")


if __name__ == "__main__":
    app = CodeforceComparator()
    app.mainloop()