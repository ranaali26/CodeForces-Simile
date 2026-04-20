import tkinter as tk
from tkinter import ttk, messagebox
import threading
from api_functions import (
    user_status, accepted_submissions, user_info,
    CodeforcesAPIError, HandleNotFoundError, APIConnectionError,
    validate_handle
)
from statistics_functions import get_problem_statistics, sort_rating


class CodeforcesSimile(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("CodeForces Simile v2.0")
        self.geometry("900x700")
        self.configure(bg="#1a1a2e")
        self.resizable(True, True)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure_styles()

        self.main_frame = ttk.Frame(self, padding="15", style="Main.TFrame")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_header()
        self.create_input_section()
        self.create_buttons_section()
        self.create_results_section()
        self.create_status_bar()

    def configure_styles(self):
        self.style.configure("Main.TFrame", background="#1a1a2e")
        self.style.configure("Header.TLabel", background="#1a1a2e", foreground="#e94560",
                             font=("Helvetica", 18, "bold"))
        self.style.configure("SubHeader.TLabel", background="#1a1a2e", foreground="#0f3460",
                             font=("Helvetica", 10))
        self.style.configure("Input.TLabel", background="#1a1a2e", foreground="#e0e0e0",
                             font=("Helvetica", 11))
        self.style.configure("Action.TButton", font=("Helvetica", 10, "bold"), padding=8)
        self.style.configure("Menu.TButton", font=("Helvetica", 10), padding=6)
        self.style.configure("Status.TLabel", background="#16213e", foreground="#a0a0a0",
                             font=("Helvetica", 9))

    def create_header(self):
        header_frame = ttk.Frame(self.main_frame, style="Main.TFrame")
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 15))

        ttk.Label(header_frame, text="⚔️ CodeForces Simile",
                  style="Header.TLabel").pack()
        ttk.Label(header_frame, text="Compare your competitive programming journey",
                  style="SubHeader.TLabel").pack()

    def create_input_section(self):
        input_frame = ttk.LabelFrame(self.main_frame, text="  Enter Handles  ", padding="15")
        input_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")

        ttk.Label(input_frame, text="Your Handle:", style="Input.TLabel").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.user_handle = ttk.Entry(input_frame, width=30, font=("Helvetica", 11))
        self.user_handle.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Friend's Handle:", style="Input.TLabel").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.friend_handle = ttk.Entry(input_frame, width=30, font=("Helvetica", 11))
        self.friend_handle.grid(row=0, column=3, padx=5, pady=5)

        self.fetch_btn = ttk.Button(input_frame, text="🔍 Fetch Data",
                                     style="Action.TButton", command=self.fetch_data_threaded)
        self.fetch_btn.grid(row=0, column=4, padx=15, pady=5)

    def create_buttons_section(self):
        buttons_frame = ttk.LabelFrame(self.main_frame, text="  Actions  ", padding="10")
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")

        button_configs = [
            ("👥 Friend's Unique Problems", 0),
            ("🏆 Your Unique Problems", 1),
            ("📊 Your Statistics", 2),
            ("📊 Friend's Statistics", 3),
            ("⚖️ Compare Statistics", 4),
        ]

        for idx, (text, cmd_idx) in enumerate(button_configs):
            ttk.Button(buttons_frame, text=text, style="Menu.TButton",
                       command=lambda x=cmd_idx: self.button_click(x)).grid(
                row=0, column=idx, padx=3, pady=3, sticky="ew"
            )
            buttons_frame.grid_columnconfigure(idx, weight=1)

    def create_results_section(self):
        results_frame = ttk.LabelFrame(self.main_frame, text="  Results  ", padding="10")
        results_frame.grid(row=3, column=0, columnspan=2, pady=5, sticky="nsew")
        self.main_frame.grid_rowconfigure(3, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.results_text = tk.Text(results_frame, height=20, width=80,
                                     font=("Consolas", 10),
                                     bg="#0f3460", fg="#e0e0e0",
                                     insertbackground="white",
                                     selectbackground="#e94560",
                                     wrap=tk.WORD)
        self.results_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(results_frame, orient="vertical",
                                   command=self.results_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.results_text.configure(yscrollcommand=scrollbar.set)

    def create_status_bar(self):
        self.status_var = tk.StringVar(value="Ready. Enter handles and fetch data to begin.")
        status_bar = ttk.Label(self.main_frame, textvariable=self.status_var,
                                style="Status.TLabel")
        status_bar.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(5, 0))

    def set_status(self, message):
        self.status_var.set(message)
        self.update_idletasks()

    def fetch_data_threaded(self):
        """Run fetch in a separate thread to prevent GUI freezing."""
        self.fetch_btn.configure(state="disabled")
        self.set_status("⏳ Fetching data...")
        thread = threading.Thread(target=self.fetch_data, daemon=True)
        thread.start()

    def fetch_data(self):
        try:
            user = validate_handle(self.user_handle.get())
            friend = validate_handle(self.friend_handle.get())

            self.set_status(f"⏳ Fetching submissions for {user}...")
            self.user_submissions = user_status(user)

            self.set_status(f"⏳ Fetching submissions for {friend}...")
            self.friend_submissions = user_status(friend)

            if self.user_submissions and self.friend_submissions:
                self.user_accepted = accepted_submissions(self.user_submissions)
                self.friend_accepted = accepted_submissions(self.friend_submissions)
                self.user_stats = get_problem_statistics(self.user_submissions)
                self.friend_stats = get_problem_statistics(self.friend_submissions)

                self.set_status(f"✅ Data loaded — {user}: {len(self.user_submissions)} submissions, "
                                f"{friend}: {len(self.friend_submissions)} submissions")
                self.after(0, lambda: messagebox.showinfo("Success", "Data fetched successfully!"))
            else:
                self.set_status("❌ Failed to fetch data")
                self.after(0, lambda: messagebox.showerror("Error", "Failed to fetch data for one or both handles!"))

        except (HandleNotFoundError, ValueError) as e:
            self.set_status(f"❌ {e}")
            self.after(0, lambda: messagebox.showerror("Error", str(e)))
        except APIConnectionError as e:
            self.set_status(f"🌐 {e}")
            self.after(0, lambda: messagebox.showerror("Connection Error", str(e)))
        except CodeforcesAPIError as e:
            self.set_status(f"⚠️ {e}")
            self.after(0, lambda: messagebox.showerror("API Error", str(e)))
        finally:
            self.after(0, lambda: self.fetch_btn.configure(state="normal"))

    def button_click(self, button_index):
        if not hasattr(self, 'user_submissions'):
            messagebox.showerror("Error", "Please fetch data first!")
            return

        self.results_text.delete(1.0, tk.END)

        if button_index == 0:
            comparison = self.friend_accepted - self.user_accepted
            self.display_comparison(comparison, "Problems solved by your friend but not by you")
        elif button_index == 1:
            comparison = self.user_accepted - self.friend_accepted
            self.display_comparison(comparison, "Problems solved by you but not by your friend")
        elif button_index == 2:
            self.display_statistics(self.user_stats, self.user_handle.get())
        elif button_index == 3:
            self.display_statistics(self.friend_stats, self.friend_handle.get())
        elif button_index == 4:
            self.compare_statistics()

    def display_comparison(self, comparison, title):
        self.results_text.insert(tk.END, f"{'='*60}\n")
        self.results_text.insert(tk.END, f"  {title}\n")
        self.results_text.insert(tk.END, f"{'='*60}\n\n")

        if not comparison:
            self.results_text.insert(tk.END, "  No problems found! 🎉\n")
            self.set_status("No problems found in this comparison")
        else:
            sorted_comparison = sorted(comparison, key=sort_rating, reverse=True)
            self.results_text.insert(tk.END, f"  {'Contest':<10} {'Index':<8} {'Name':<30} {'Rating':<8}\n")
            self.results_text.insert(tk.END, f"  {'-'*56}\n")

            for problem in sorted_comparison:
                parts = problem.split('-')
                if len(parts) >= 4:
                    self.results_text.insert(tk.END,
                                              f"  {parts[0]:<10} {parts[1]:<8} {parts[2]:<30} {parts[3]:<8}\n")
                else:
                    self.results_text.insert(tk.END, f"  {problem}\n")

            self.set_status(f"Found {len(comparison)} problems")

    def display_statistics(self, stats, handle):
        self.results_text.insert(tk.END, f"{'='*60}\n")
        self.results_text.insert(tk.END, f"  Statistics for {handle}\n")
        self.results_text.insert(tk.END, f"{'='*60}\n\n")

        self.results_text.insert(tk.END, f"  Total Submissions:        {stats['total_submissions']}\n")
        self.results_text.insert(tk.END, f"  Accepted Submissions:     {stats['accepted_submissions']}\n")
        self.results_text.insert(tk.END, f"  Unique Accepted Problems: {stats['unique_accepted_problems']}\n")
        self.results_text.insert(tk.END, f"  Acceptance Rate:          {stats['acceptance_rate']}%\n")
        self.results_text.insert(tk.END, f"  Avg Attempts Before AC:   {stats['average_attempts_before_ac']}\n")

        self.results_text.insert(tk.END, f"\n  Problem Ratings Distribution:\n")
        self.results_text.insert(tk.END, f"  {'-'*40}\n")
        for rating, count in sorted(stats['problem_ratings'].items()):
            bar = "█" * min(count, 30)
            self.results_text.insert(tk.END, f"  Rating {rating:>6}: {count:>3} {bar}\n")

        self.results_text.insert(tk.END, f"\n  Top Languages:\n")
        self.results_text.insert(tk.END, f"  {'-'*40}\n")
        for lang, count in sorted(stats['languages_used'].items(), key=lambda x: x[1], reverse=True)[:5]:
            self.results_text.insert(tk.END, f"  {lang:<25}: {count}\n")

        self.results_text.insert(tk.END, f"\n  Verdicts Distribution:\n")
        self.results_text.insert(tk.END, f"  {'-'*40}\n")
        for verdict, count in sorted(stats['verdicts_distribution'].items(), key=lambda x: x[1], reverse=True):
            self.results_text.insert(tk.END, f"  {verdict:<25}: {count}\n")

        self.set_status(f"Showing statistics for {handle}")

    def compare_statistics(self):
        user = self.user_handle.get().strip()
        friend = self.friend_handle.get().strip()

        self.results_text.insert(tk.END, f"{'='*60}\n")
        self.results_text.insert(tk.END, f"  ⚖️ Comparison: {user} vs {friend}\n")
        self.results_text.insert(tk.END, f"{'='*60}\n\n")

        self.results_text.insert(tk.END, f"  {'Metric':<25} {user:<15} {friend:<15} {'Winner':<10}\n")
        self.results_text.insert(tk.END, f"  {'-'*65}\n")

        metrics = [
            ('Total Submissions', 'total_submissions', True),
            ('Accepted Submissions', 'accepted_submissions', True),
            ('Unique Accepted', 'unique_accepted_problems', True),
            ('Acceptance Rate (%)', 'acceptance_rate', True),
            ('Avg Attempts', 'average_attempts_before_ac', False),
        ]

        for name, key, higher_is_better in metrics:
            u_val = self.user_stats[key]
            f_val = self.friend_stats[key]

            if isinstance(u_val, (int, float)) and isinstance(f_val, (int, float)):
                if higher_is_better:
                    winner = "👈" if u_val >= f_val else "👉"
                else:
                    winner = "👈" if u_val <= f_val else "👉"
            else:
                winner = ""

            self.results_text.insert(tk.END,
                                      f"  {name:<25} {str(u_val):<15} {str(f_val):<15} {winner}\n")

        self.set_status(f"Comparing {user} vs {friend}")


if __name__ == "__main__":
    app = CodeforcesSimile()
    app.mainloop()