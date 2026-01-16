import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker
import numpy as np
import requests
import threading

class RaceComparatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Global Race Comparator")
        self.root.geometry("950x650")

        # --- Data Configuration ---
        self.track_distances = ["100m", "200m", "400m", "800m", "1600m", "3200m"]
        self.xc_distances = ["1 Mile", "2 Miles", "3 Miles"]
        
        # Baselines: Approximate World Records in Seconds (as of ~2024)
        # Used as the "Anchor" for the simulation.
        self.wr_baselines = {
            "Male": {
                "100m": 9.58, "200m": 19.19, "400m": 43.03, "800m": 100.91, 
                "1600m": 223.13, "3200m": 478.0, 
                "1 Mile": 223.13, "2 Miles": 478.0, "3 Miles": 755.0 
            },
            "Female": {
                "100m": 10.49, "200m": 21.34, "400m": 47.60, "800m": 113.28, 
                "1600m": 247.0, "3200m": 530.0, 
                "1 Mile": 247.0, "2 Miles": 530.0, "3 Miles": 845.0
            }
        }

        # --- GUI Layout ---
        self.create_widgets()
        
        # --- Initialize Cloud Counter ---
        threading.Thread(target=self.update_visitor_count, daemon=True).start()

    def create_widgets(self):
        # Styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", font=("Helvetica", 11))
        style.configure("TButton", font=("Helvetica", 11, "bold"))

        # Main Layout
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left Panel (Controls)
        controls_frame = ttk.LabelFrame(main_frame, text="  Runner Profile  ", padding="15")
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20), ipadx=10)

        # Inputs
        ttk.Label(controls_frame, text="Age (10-50):").pack(anchor=tk.W, pady=(5, 0))
        self.age_var = tk.StringVar(value="20")
        self.age_combo = ttk.Combobox(controls_frame, textvariable=self.age_var, state="readonly", width=10)
        self.age_combo['values'] = [str(i) for i in range(10, 51)]
        self.age_combo.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(controls_frame, text="Sex:").pack(anchor=tk.W)
        self.sex_var = tk.StringVar(value="Male")
        frame_sex = ttk.Frame(controls_frame)
        frame_sex.pack(fill=tk.X, pady=(0, 15))
        ttk.Radiobutton(frame_sex, text="Male", variable=self.sex_var, value="Male").pack(side=tk.LEFT, padx=(0,10))
        ttk.Radiobutton(frame_sex, text="Female", variable=self.sex_var, value="Female").pack(side=tk.LEFT)

        ttk.Separator(controls_frame, orient='horizontal').pack(fill='x', pady=10)

        ttk.Label(controls_frame, text="Event Type:").pack(anchor=tk.W)
        self.event_type_var = tk.StringVar(value="Track")
        self.event_type_var.trace('w', self.update_distance_options) 
        frame_type = ttk.Frame(controls_frame)
        frame_type.pack(fill=tk.X, pady=(0, 15))
        ttk.Radiobutton(frame_type, text="Track", variable=self.event_type_var, value="Track").pack(side=tk.LEFT, padx=(0,10))
        ttk.Radiobutton(frame_type, text="Cross Country", variable=self.event_type_var, value="XC").pack(side=tk.LEFT)

        ttk.Label(controls_frame, text="Distance:").pack(anchor=tk.W, pady=(5, 0))
        self.dist_combo = ttk.Combobox(controls_frame, state="readonly")
        self.dist_combo.pack(fill=tk.X, pady=(0, 15))
        self.update_distance_options() 

        ttk.Label(controls_frame, text="Your Time (MM:SS):").pack(anchor=tk.W, pady=(5, 0))
        self.time_entry = ttk.Entry(controls_frame)
        self.time_entry.insert(0, "05:00")
        self.time_entry.pack(fill=tk.X, pady=(0, 25))

        # Button
        self.calc_btn = ttk.Button(controls_frame, text="COMPARE SCORE", command=self.generate_plot)
        self.calc_btn.pack(fill=tk.X, ipady=5)

        # Visitor Counter Label
        self.counter_label = ttk.Label(controls_frame, text="Connecting to user db...", font=("Arial", 8), foreground="gray")
        self.counter_label.pack(side=tk.BOTTOM, pady=10)

        # Right Panel (Matplotlib)
        self.graph_frame = ttk.Frame(main_frame, borderwidth=2, relief="sunken")
        self.graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.figure, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.figure.patch.set_facecolor('#f0f0f0') # Match GUI background roughly
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_distance_options(self, *args):
        if self.event_type_var.get() == "Track":
            self.dist_combo['values'] = self.track_distances
            self.dist_combo.set("1600m")
        else:
            self.dist_combo['values'] = self.xc_distances
            self.dist_combo.set("3 Miles")

    def parse_time(self, time_str):
        try:
            parts = time_str.split(":")
            if len(parts) != 2: raise ValueError
            minutes = int(parts[0])
            seconds = int(parts[1])
            return minutes * 60 + seconds
        except ValueError:
            return None

    def update_visitor_count(self):
        try:
            # Using a public countapi.xyz key. 
            # In a real app, replace 'github_runner_tool_v1' with a new unique string if this one gets spammed.
            url = "https://api.countapi.xyz/hit/race_comparator_tool_gen2/visits"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                count = response.json().get("value", 0)
                self.root.after(0, lambda: self.counter_label.config(text=f"Community Users: {count}"))
            else:
                raise Exception
        except:
            self.root.after(0, lambda: self.counter_label.config(text="Users: Offline Mode"))

    def get_age_factor(self, age):
        # Simulation of Age Grading
        # Peak performance assumed roughly 20-30
        # Younger than 15: Significantly slower (developing)
        # Older than 30: Gradual decline
        if 20 <= age <= 30:
            return 1.0
        elif age < 20:
            # Steep curve for kids
            return 1.0 + ((20 - age) * 0.04) 
        else:
            # Gradual curve for masters
            return 1.0 + ((age - 30) * 0.015)

    def generate_plot(self):
        # 1. Validation
        user_time_str = self.time_entry.get()
        user_seconds = self.parse_time(user_time_str)
        if user_seconds is None:
            messagebox.showerror("Input Error", "Format must be MM:SS (e.g. 04:30)")
            return

        age = int(self.age_var.get())
        sex = self.sex_var.get()
        dist = self.dist_combo.get()

        # 2. Advanced Data Simulation
        # Step A: Get World Record Baseline
        wr_seconds = self.wr_baselines[sex][dist]
        
        # Step B: Apply Age Grading to the "Baseline" (The theoretical best for that age)
        age_factor = self.get_age_factor(age)
        age_adjusted_baseline = wr_seconds * age_factor

        # Step C: Simulate the "Population"
        # The general pool is not elite. We assume the mean of the public 
        # is roughly 2.0x the World Record time for that demographic.
        # Short sprints have less variance (1.5x), long distance has more (2.2x).
        
        if "100m" in dist or "200m" in dist:
            pool_mean_factor = 1.6
            pool_std_dev_percent = 0.15 
        elif "400m" in dist or "800m" in dist:
            pool_mean_factor = 1.8
            pool_std_dev_percent = 0.20
        else:
            pool_mean_factor = 2.1 # Distance runners vary wildly
            pool_std_dev_percent = 0.25

        pool_mean = age_adjusted_baseline * pool_mean_factor
        pool_std = pool_mean * pool_std_dev_percent
        
        # Generate 5,000 data points
        data = np.random.normal(pool_mean, pool_std, 5000)
        
        # Filter unrealistic times (nobody runs faster than WR)
        data = data[data > age_adjusted_baseline] 

        # 3. Plotting
        self.ax.clear()
        
        # Plot Histogram
        n, bins, patches = self.ax.hist(data, bins=40, color='#3498db', alpha=0.7, edgecolor='white')
        
        # Plot User Line
        self.ax.axvline(user_seconds, color='#e74c3c', linestyle='-', linewidth=3, label='Your Time')
        
        # Add a text annotation for the user
        self.ax.text(user_seconds, self.ax.get_ylim()[1]*0.95, f" You\n {user_time_str}", 
                     color='#e74c3c', ha='center', fontweight='bold')

        # Formatting
        self.ax.set_title(f"Performance Distribution: {dist} ({sex}, Age {age})", fontweight='bold', pad=15)
        self.ax.set_ylabel("Frequency", fontsize=10)
        self.ax.set_xlabel("Time (Seconds)", fontsize=10)
        
        # Make X-Axis simpler to read
        self.ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=8))
        
        self.ax.grid(axis='y', alpha=0.3, linestyle='--')
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = RaceComparatorApp(root)
    root.mainloop()
