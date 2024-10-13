import csv
import matplotlib.pyplot as plt
from environment import create_ship_layout
from fire import spread_fire
from bonus import move_bot_bonus
import numpy as np
import os


# Create a folder named "bot2" if it doesn't exist
if not os.path.exists("bot5"):
    os.makedirs("bot5")

# Function to run the simulation and track success rate for multiple iterations
def run_simulation(size, q, iterations, csv_file):
    success_count = 0
    success_rates = []

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Iteration", "Success Rate (%)"])  # CSV header

        for iteration in range(1, iterations + 1):
            matrix, bot_initial_position, button_position, fire_cells = create_ship_layout(size, q)
            button_pressed = False

            while not button_pressed:
                fire_cells = spread_fire(matrix, fire_cells, q)
                bot_initial_position, button_pressed, path = move_bot_bonus(matrix, bot_initial_position, button_position, fire_cells)

                # Check if bot steps into fire
                if bot_initial_position in fire_cells:
                    break

            if button_pressed:
                success_count += 1

            success_rate = (success_count / iteration) * 100
            success_rates.append(success_rate)
            
            # Save success rate to CSV
            writer.writerow([iteration, success_rate])

            print(f"q={q:.1f}, Iteration {iteration}: Success Rate = {success_rate:.2f}%")

    return success_rates, success_count / iterations * 100  # Return success rates and final accuracy

# Function to plot success rate over iterations
def plot_success_rate(success_rates, q):
    plt.plot(range(1, len(success_rates) + 1), success_rates, marker='o', linestyle='-', color='b')
    plt.xlabel('Iteration')
    plt.ylabel('Cumulative Success Rate (%)')
    plt.title(f'Cumulative Success Rate for q={q:.1f} over Iterations')
    plt.grid(True)
    plt.savefig(f'bot5/success_rate_bot5_1000_q_{q:.1f}.png')  # Save plot as image
    plt.close()  # Close the plot to avoid overlapping

# Run simulations for multiple q values and track final accuracies
size = 40  # Grid size
num_iterations = 250  # Number of iterations per q
q_values = np.arange(0.1, 1.1, 0.1)# Different fire spread probabilities

final_accuracies = []

for q in q_values:
    print(f"Running simulation for q={q}")
    success_rates, final_accuracy = run_simulation(size, q, num_iterations, f'bot5/success_rates_bot5_1000_q_{q:.1f}.csv')
    final_accuracies.append(final_accuracy)

    # Plot success rate for this q value
    plot_success_rate(success_rates, q)

# Plot final accuracies vs q values
plt.plot(q_values, final_accuracies, marker='o', linestyle='-', color='r')
plt.xlabel('Fire Spread Probability (q)')
plt.ylabel('Final Accuracy (%)')
plt.title('Final Accuracy vs Fire Spread Probability (q)')
plt.grid(True)
plt.savefig('bot5/final_accuracy_bot5_1000_vs_q.png')  # Save plot as image
plt.show()