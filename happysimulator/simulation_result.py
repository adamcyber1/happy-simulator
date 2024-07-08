import math

from matplotlib import pyplot as plt

from happysimulator.datasink import DataSink


class SimulationResult:

    # TODO further subclass the data sink types
    def __init__(self, sinks: list[DataSink]):
        self._sinks = sinks

    def print_summary(self):
        raise NotImplementedError("Implement me!")

    """
    This code does its best to pretty-display the simulation result, but ultimately you may need to work with the 
    raw CSV / dataframe data to create graphics that best suit your need.
    """
    def display_graphs(self):
        num_plots = len(self._sinks)

        # Calculate the number of columns and rows for the subplot grid
        if num_plots == 4:
            num_columns = num_rows = 2
        else:
            num_columns = int(math.ceil(num_plots ** 0.5))
            num_rows = num_plots // num_columns + (num_plots % num_columns > 0)

        plt.figure(figsize=(10 * num_columns, 6 * num_rows))
        plt.rcParams['figure.facecolor'] = 'lightgrey'
        plt.rcParams['axes.facecolor'] = 'lightgrey'

        # Determine global x-axis range
        global_x_min = float('inf')
        global_x_max = float('-inf')
        for sink in self._sinks:
            x_min = sink.df['TIME_SECONDS'].min()
            x_max = sink.df['TIME_SECONDS'].max()
            if x_min < global_x_min:
                global_x_min = x_min
            if x_max > global_x_max:
                global_x_max = x_max

        for i, sink in enumerate(self._sinks, start=1):
            ax = plt.subplot(num_rows, num_columns, i)
            min_values = []
            max_values = []
            for stat_name in sink.stat_names:
                ax.plot(sink.df['TIME_SECONDS'], sink.df[stat_name], marker='o', markersize=4, linestyle='-', label=stat_name)
                min_values.append(sink.df[stat_name].min())
                max_values.append(sink.df[stat_name].max())

            global_y_min = max(0, min(min_values))
            global_y_max = max(0, max(max_values))

            ax.set_xlim(global_x_min, global_x_max)  # Set global x-axis limits
            ax.set_ylim(0.9 * global_y_min, 1.1 * global_y_max)
            ax.set_title(f"{sink.name} [{', '.join(sink.stat_names)}]", fontsize=16)
            ax.set_xlabel('Time (Seconds)', fontsize=14)
            ax.set_ylabel('Value', fontsize=14)
            ax.grid(True, color='gray')
            ax.legend()

        plt.tight_layout(pad=3.0)
        plt.show()

    def print_csv(self):
         for sink in self._sinks:
             print(sink.generate_csv())

    def save_graphs(self, directory: str):
        pass

    def save_csvs(self, directory: str):
        for sink in self._sinks:
            sink.save_csv(directory=directory)
