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
        num_columns = int(num_plots ** 0.5) + 1
        num_rows = num_plots // num_columns + (num_plots % num_columns > 0)

        plt.figure(figsize=(10 * num_columns, 6 * num_rows))
        plt.rcParams['figure.facecolor'] = 'lightgrey'
        plt.rcParams['axes.facecolor'] = 'lightgrey'

        for i, sink in enumerate(self._sinks, start=1):
            ax = plt.subplot(num_rows, num_columns, i)
            min_values = []
            max_values = []
            for stat_name in sink.stat_names:
                ax.plot(sink.df['TIME_SECONDS'], sink.df[stat_name], marker='o', markersize=4, linestyle='-', label=stat_name)
                # Collecting min and max values across all stats for this sink
                min_values.append(sink.df[stat_name].min())
                max_values.append(sink.df[stat_name].max())

            # Determining the global min and max for the current sink's stats
            global_min = min(min_values)
            global_max = max(max_values)

            # Setting y-axis limits to include all stats
            ax.set_ylim(0.9 * global_min, 1.1 * global_max)  # Adjusted to show a bit more space around the min/max values
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
