import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, Label, Button, Entry, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Loading data from user's csv file
def load_data():
    file_path = filedialog.askopenfilename(title="Select a CSV file", filetypes=[("CSV files", "*.csv")])
    if file_path:
        global df
        df = pd.read_csv(file_path)
        col_select_window(df)

def col_select_window(df):
    col_select = Tk()
    col_select.title("Column Selection")

    # Entries for column selection
    Label(col_select, text="Enter column names (comma-separated):").pack()
    entry = Entry(col_select)
    entry.pack()
    entry.focus_set()

    notebook = ttk.Notebook(col_select)

    # Create tabs for graphs
    histogram_tab = ttk.Frame(notebook)
    bar_graph_tab = ttk.Frame(notebook)
    boxplot_tab = ttk.Frame(notebook)

    notebook.add(histogram_tab, text="Histogram")
    notebook.add(bar_graph_tab, text="Bar Graph")
    notebook.add(boxplot_tab, text="Box Plot")

    notebook.pack(expand=1, fill="both")

    # Apply statistics based on selected columns
    def calculate_statistics():
        selected_cols = [col.strip() for col in entry.get().replace(" ", "").split(",")]
        selected_df = df[selected_cols]
        descriptive_stats = selected_df.describe()
        print(descriptive_stats)

        # Histogram
        plt.figure(figsize=(8, 6))
        plt.subplot(111, frame_on=False)
        plt.axis('off')
        selected_df.hist(bins=20, ax=plt.gca())
        plt.title("Histogram")
        plt.subplots_adjust(top=0.9)
        plt.tight_layout()

        histogram_canvas = FigureCanvasTkAgg(plt.gcf(), master=histogram_tab)
        histogram_canvas.draw()
        histogram_canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

        # Numerical labels to histograms
        for ax in histogram_canvas.figure.axes:
            ax.set_title(selected_df.columns[histogram_canvas.figure.axes.index(ax)])
            ax.set_xlabel(selected_df.columns[histogram_canvas.figure.axes.index(ax)])
            ax.set_ylabel("Frequency")
            ax.set_xticks(np.arange(selected_df.min().min(), selected_df.max().max(), 1))
            ax.set_xticklabels(np.arange(selected_df.min().min(), selected_df.max().max(), 1))

        # Bar graph
        plt.figure(figsize=(8, 6))
        selected_df.mean().plot(kind='bar', color='skyblue')
        plt.title("Bar Graph")
        plt.xlabel("Columns")
        plt.ylabel("Mean")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        bar_graph_canvas = FigureCanvasTkAgg(plt.gcf(), master=bar_graph_tab)
        bar_graph_canvas.draw()
        bar_graph_canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

        # Box plot
        plt.figure(figsize=(8, 6))
        plt.subplot(111, frame_on=False)
        plt.axis('off')
        selected_df.boxplot(ax=plt.gca())
        plt.title("Box Plot")
        plt.subplots_adjust(top=0.9)
        plt.tight_layout()

        for i in range(len(selected_cols)):
            x = np.random.normal(i + 1, 0.04, size=len(selected_df[selected_cols[i]]))
            plt.scatter(x, selected_df[selected_cols[i]], alpha=0.5)

        plt.xticks(np.arange(1, len(selected_cols) + 1), selected_cols)

        boxplot_canvas = FigureCanvasTkAgg(plt.gcf(), master=boxplot_tab)
        boxplot_canvas.draw()
        boxplot_canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

    Button(col_select, text="Calculate", command=calculate_statistics).pack()

def main():
    root = Tk()
    root.title("Descriptive Statistics Tool")

    label = Label(root, text="Click the button to load a CSV file:")
    label.pack()

    load_button = Button(root, text="Load Data", command=load_data)
    load_button.pack()

    root.mainloop()
# Initalize
if __name__ == "__main__":
    main()
