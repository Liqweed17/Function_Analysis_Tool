import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import sympy as sp
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math


class FunctionAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Function Analysis Tool")
        self.root.geometry("800x750")
        self.root.configure(bg='#f0f5ff')  # Light blue background

        # Create a scrollable canvas
        self.canvas = tk.Canvas(root, bg='#f0f5ff')
        self.scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#f0f5ff')

        # Configure the canvas and scrollbar
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Color scheme
        self.colors = {
            'background': '#f0f5ff',
            'card': '#ffffff',
            'primary': '#1e88e5',
            'text': '#333333',
            'secondary_text': '#555555',
            'border': '#bbdefb',
            'function': '#1e88e5',
            'derivative': '#f44336',
            'integral': '#4caf50',
            'highlight': '#e3f2fd'
        }

        # Main container
        self.main_frame = tk.Frame(self.scrollable_frame, bg=self.colors['background'], padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        title_frame.pack(fill=tk.X, pady=(0, 15))
        tk.Label(title_frame, text="Function Analysis Tool",
                 font=('Helvetica', 16, 'bold'),
                 bg=self.colors['background'],
                 fg=self.colors['primary']).pack()

        # Function Input Card
        input_card = tk.Frame(self.main_frame, bg=self.colors['card'],
                              padx=15, pady=15, relief=tk.RAISED, bd=1,
                              highlightbackground=self.colors['border'],
                              highlightthickness=1)
        input_card.pack(fill=tk.X, pady=5)

        tk.Label(input_card, text="Enter a Function (Python Syntax)",
                 font=('Helvetica', 12, 'bold'),
                 bg=self.colors['card'],
                 fg=self.colors['primary']).pack(anchor=tk.W, pady=(0, 10))

        example_frame = tk.Frame(input_card, bg=self.colors['card'])
        example_frame.pack(fill=tk.X, pady=5)
        tk.Label(example_frame, text="Example: x**2 + 3*x + 5",
                 font=('Courier', 10),
                 bg=self.colors['card'],
                 fg=self.colors['primary']).pack(side=tk.LEFT)

        self.function_entry = tk.Entry(input_card, font=('Courier', 12),
                                       bd=1, relief=tk.SOLID, highlightthickness=1,
                                       highlightbackground=self.colors['border'])
        self.function_entry.pack(fill=tk.X, pady=5)
        self.function_entry.insert(0, "x**2 + 3*x + 5")

        submit_btn = tk.Button(input_card, text="Submit",
                               font=('Helvetica', 10, 'bold'),
                               bg=self.colors['primary'],
                               fg='white',
                               activebackground='#1565c0',
                               activeforeground='white',
                               relief=tk.FLAT,
                               command=self.analyze_function)
        submit_btn.pack(pady=5, ipadx=10, ipady=5)

        # Options Card
        options_card = tk.Frame(self.main_frame, bg=self.colors['card'],
                                padx=15, pady=15, relief=tk.RAISED, bd=1,
                                highlightbackground=self.colors['border'],
                                highlightthickness=1)
        options_card.pack(fill=tk.X, pady=5)

        tk.Label(options_card, text="Select Options",
                 font=('Helvetica', 12, 'bold'),
                 bg=self.colors['card'],
                 fg=self.colors['primary']).pack(anchor=tk.W, pady=(0, 10))

        range_frame = tk.Frame(options_card, bg=self.colors['card'])
        range_frame.pack(fill=tk.X, pady=5)

        tk.Label(range_frame, text="Select Range of x values",
                 font=('Helvetica', 10),
                 bg=self.colors['card'],
                 fg=self.colors['text']).pack(side=tk.LEFT, padx=5)

        min_frame = tk.Frame(range_frame, bg=self.colors['card'])
        min_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(min_frame, text="Min",
                 font=('Helvetica', 10),
                 bg=self.colors['card'],
                 fg=self.colors['text']).pack()
        self.min_entry = tk.Entry(min_frame, width=8, font=('Helvetica', 10),
                                  bd=1, relief=tk.SOLID,
                                  highlightbackground=self.colors['border'])
        self.min_entry.pack()
        self.min_entry.insert(0, "-5")

        max_frame = tk.Frame(range_frame, bg=self.colors['card'])
        max_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(max_frame, text="Max",
                 font=('Helvetica', 10),
                 bg=self.colors['card'],
                 fg=self.colors['text']).pack()
        self.max_entry = tk.Entry(max_frame, width=8, font=('Helvetica', 10),
                                  bd=1, relief=tk.SOLID,
                                  highlightbackground=self.colors['border'])
        self.max_entry.pack()
        self.max_entry.insert(0, "5")

        operation_frame = tk.Frame(options_card, bg=self.colors['card'])
        operation_frame.pack(fill=tk.X, pady=10)

        tk.Label(operation_frame, text="Choose Operation:",
                 font=('Helvetica', 10),
                 bg=self.colors['card'],
                 fg=self.colors['text']).pack(side=tk.LEFT, padx=5)

        self.operation_var = tk.StringVar(value="diff")

        tk.Radiobutton(operation_frame, text="Differentiation",
                       variable=self.operation_var, value="diff",
                       font=('Helvetica', 10),
                       bg=self.colors['card'],
                       fg=self.colors['primary'],
                       selectcolor=self.colors['card'],
                       activebackground=self.colors['card'],
                       activeforeground=self.colors['primary']).pack(side=tk.LEFT, padx=5)

        tk.Radiobutton(operation_frame, text="Integration",
                       variable=self.operation_var, value="int",
                       font=('Helvetica', 10),
                       bg=self.colors['card'],
                       fg=self.colors['primary'],
                       selectcolor=self.colors['card'],
                       activebackground=self.colors['card'],
                       activeforeground=self.colors['primary']).pack(side=tk.LEFT, padx=5)

        tk.Radiobutton(operation_frame, text="Both",
                       variable=self.operation_var, value="both",
                       font=('Helvetica', 10),
                       bg=self.colors['card'],
                       fg=self.colors['primary'],
                       selectcolor=self.colors['card'],
                       activebackground=self.colors['card'],
                       activeforeground=self.colors['primary']).pack(side=tk.LEFT, padx=5)

        # Graph Visualization Card
        graph_card = tk.Frame(self.main_frame, bg=self.colors['card'],
                              padx=15, pady=15, relief=tk.RAISED, bd=1,
                              highlightbackground=self.colors['border'],
                              highlightthickness=1)
        graph_card.pack(fill=tk.BOTH, expand=True, pady=5)

        tk.Label(graph_card, text="Graph Visualization",
                 font=('Helvetica', 12, 'bold'),
                 bg=self.colors['card'],
                 fg=self.colors['primary']).pack(anchor=tk.W, pady=(0, 10))

        self.figure = plt.Figure(figsize=(8, 4), dpi=100, facecolor=self.colors['card'])
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor(self.colors['card'])

        self.canvas_plot = FigureCanvasTkAgg(self.figure, master=graph_card)
        self.canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Results Card
        results_card = tk.Frame(self.main_frame, bg=self.colors['card'],
                                padx=15, pady=15, relief=tk.RAISED, bd=1,
                                highlightbackground=self.colors['border'],
                                highlightthickness=1)
        results_card.pack(fill=tk.BOTH, expand=True, pady=5)

        tk.Label(results_card, text="Results",
                 font=('Helvetica', 12, 'bold'),
                 bg=self.colors['card'],
                 fg=self.colors['primary']).pack(anchor=tk.W, pady=(0, 10))

        # Scrollable frame for results
        scrollable_frame = tk.Frame(results_card, bg=self.colors['card'])
        scrollable_frame.pack(fill=tk.BOTH, expand=True)

        # Add scrollbar
        scrollbar = tk.Scrollbar(scrollable_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add Text widget and link it to the scrollbar
        self.results_text = tk.Text(scrollable_frame, wrap=tk.WORD, font=('Courier', 10),
                                    bg=self.colors['card'], fg=self.colors['text'],
                                    height=10, relief=tk.SOLID, bd=1,
                                    yscrollcommand=scrollbar.set)
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure scrollbar
        scrollbar.config(command=self.results_text.yview)

    def parse_function(self, func_str):
        x = sp.symbols('x')
        try:
            func_str = func_str.replace('^', '**')
            expr = sp.sympify(func_str)
            f = sp.lambdify(x, expr, modules=['numpy', 'math'])
            return f, expr
        except (sp.SympifyError, TypeError) as e:
            messagebox.showerror("Error", f"Invalid function input: {str(e)}")
            return None, None

    def numerical_derivative(self, f, x_vals):
        dx = x_vals[1] - x_vals[0]
        deriv_vals = np.gradient(f(x_vals), dx)
        return deriv_vals

    def numerical_integral(self, f, a, b):
        integral_val, _ = quad(f, a, b)
        return integral_val

    def integral_function(self, f, x_vals):
        integral_vals = []
        a = x_vals[0]
        for b in x_vals:
            val, _ = quad(f, a, b)
            integral_vals.append(val)
        return np.array(integral_vals)

    def analyze_function(self):
        func_str = self.function_entry.get().strip()
        if not func_str:
            messagebox.showerror("Error", "Please enter a function")
            return

        f, expr = self.parse_function(func_str)
        if f is None:
            return

        try:
            x_min = float(self.min_entry.get())
            x_max = float(self.max_entry.get())
            if x_max <= x_min:
                messagebox.showerror("Error", "Max x must be greater than min x.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid numeric input for range.")
            return

        operation = self.operation_var.get()

        x_vals = np.linspace(x_min, x_max, 500)
        try:
            f_vals = f(x_vals)
        except Exception as e:
            messagebox.showerror("Error", f"Error evaluating function: {str(e)}")
            return

        show_derivative = operation in ['diff', 'both']
        show_integral = operation in ['int', 'both']

        deriv_vals = None
        integral_vals = None

        self.ax.clear()
        self.results_text.delete(1.0, tk.END)

        # Plot original function
        self.ax.plot(x_vals, f_vals, label=f'f(x) = {str(expr)}',
                    color=self.colors['function'], linewidth=2)

        if show_derivative:
            try:
                deriv_vals = self.numerical_derivative(f, x_vals)
                self.ax.plot(x_vals, deriv_vals, label='Derivative',
                            color=self.colors['derivative'], linewidth=2)

                x_sym = sp.symbols('x')
                deriv_expr = sp.diff(expr, x_sym)
                self.results_text.insert(tk.END, "=== DERIVATIVE ===\n")
                self.results_text.insert(tk.END, f"f'(x) = {str(deriv_expr)}\n")
                self.results_text.insert(tk.END, f"At x={x_min}: {deriv_vals[0]:.4f}\n")
                self.results_text.insert(tk.END, f"At x={x_max}: {deriv_vals[-1]:.4f}\n\n")
            except Exception as e:
                self.results_text.insert(tk.END, f"Derivative Error: {str(e)}\n\n")

        if show_integral:
            try:
                integral_vals = self.integral_function(f, x_vals)
                self.ax.plot(x_vals, integral_vals, label='Integral',
                            color=self.colors['integral'], linewidth=2)

                x_sym = sp.symbols('x')
                integral_expr = sp.integrate(expr, x_sym)
                definite_integral = self.numerical_integral(f, x_min, x_max)
                
                self.results_text.insert(tk.END, "=== INTEGRAL ===\n")
                self.results_text.insert(tk.END, f"∫f(x)dx = {str(integral_expr)} + C\n")
                self.results_text.insert(tk.END, f"Definite integral ({x_min} to {x_max}): {definite_integral:.4f}\n\n")
            except Exception as e:
                self.results_text.insert(tk.END, f"Integral Error: {str(e)}\n\n")

        # Configure plot
        self.ax.set_title('Function Analysis', color=self.colors['text'])
        self.ax.set_xlabel('x', color=self.colors['text'])
        self.ax.set_ylabel('y', color=self.colors['text'])
        self.ax.legend()
        self.ax.grid(True, color=self.colors['border'], linestyle='--', alpha=0.5)
        self.ax.tick_params(colors=self.colors['text'])

        for spine in self.ax.spines.values():
            spine.set_color(self.colors['border'])

        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = FunctionAnalyzerApp(root)
    root.mainloop()