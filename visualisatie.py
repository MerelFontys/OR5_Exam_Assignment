import matplotlib.pyplot as plt 
def plot_sa_progress (current_objective_history, best_objective_history, run_number):
    iterations = range(1, len(current_objective_history) + 1)

    plt.figure(figsize = (10 , 5))

    #lijn van huidige oplossing
    plt.plot(iterations, current_objective_history, label = "Current Solution")
    #lijn van beste oplossing
    plt.plot(iterations,best_objective_history, label = "Best Solution")
    #Temperatuur
    plt.xlabel("Iteration")
    plt.ylabel("Total tardiness")
    plt.title("Simulated Annealing objective values - run "+ str(run_number))
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()

def plot_schedule(schedule_data):

    # Machines ophalen
    machine_names = list(dict.fromkeys(row["Machine"] for row in schedule_data))

    # Een aparte Gantt-chart per machine
    for machine in machine_names:
        # Orders van deze machine ophalen
        machine_schedule = [row for row in schedule_data if row["Machine"] == machine]

        start_times = []
        completion_times = []
        tardiness_values = []
        current_time = 0

        # Calculate start time, completion time and tardiness
        for row in machine_schedule:
            start_times.append(row["Start"])
            completion_times.append(row["End"])
            tardiness_values.append(row["Tardiness"])

        # Create Gantt chart
        fig, ax = plt.subplots(figsize=(10, 5))

        for position in range(len(machine_schedule)):
            row = machine_schedule[position]

            # Processing interval
            ax.barh(position, row["Process"], left=row["Start"])
            # Job name inside the bar
            ax.text(row["Start"] + row["Process"] / 2, position, str(row["Order"]), ha="center",va="center")
            # Due date marker
            ax.plot(row["Deadline"], position,marker="v",markeredgecolor="black",markeredgewidth=0.8)
            # Dashed line from due date to completion time
            ax.hlines(
                position,
                row["Deadline"],
                row["End"],
                colors="red" if row["Tardiness"] > 0 else "lightgray",
                linestyles="--",
                linewidth=0.8
            )

        # Labels for the jobs
        y_labels = []
        for position in range(len(machine_schedule)):
            row = machine_schedule[position]
            label = str(row["Order"])
            if row["Tardiness"] > 0:
                label = label + f"(T = {row["Tardiness"]:.4f})"

            y_labels.append(label)

        ax.set_yticks(range(len(machine_schedule)))
        ax.set_yticklabels(y_labels)
        ax.set_xlabel("Time")
        ax.set_ylabel("Orders")
        ax.set_title(f"Schedule for {machine} with total tardiness = "f"{sum(tardiness_values):.4f}")

        # First scheduled job at the top
        ax.invert_yaxis()
        ax.grid(axis="x")
        plt.tight_layout()
        plt.show()