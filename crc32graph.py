import pandas as pd
import matplotlib.pyplot as plt

def plot_execution_times(csv_file, plot_filename, dataset_type):
    """
    Function to plot execution times and save the plot.
    
    Parameters:
    csv_file (str): Path to the CSV file.
    plot_filename (str): The file name to save the plot.
    dataset_type (str): Either 'encode' or 'validate', used for labeling.
    """
    # Load the CSV file
    data = pd.read_csv(csv_file)

    # Plotting the data
    plt.figure(figsize=(10, 6))

    # Plot Exec_Time_With_Tests
    plt.plot(data['Lines_Read'], data['Exec_Time_With_Tests'], label=f'{dataset_type.capitalize()} - No Tests', color='b', marker='o')

    # Plot Exec_Time_No_Tests
    plt.plot(data['Lines_Read'], data['Exec_Time_No_Tests'], label=f'{dataset_type.capitalize()} - With Tests', color='r', marker='x')

    # Adding titles and labels
    plt.title(f'Execution Time Comparison for {dataset_type.capitalize()} Data: With and Without Tests')
    plt.xlabel('Number of Lines Read from the Beginning of the File')
    plt.ylabel('Execution Time (seconds)')
    plt.legend()

    # Display grid for better visibility
    plt.grid(True)

    # Adjust layout to avoid clipping labels
    plt.tight_layout()

    # Save the plot as a PNG file
    plt.savefig(plot_filename)

    # Optionally, you can save the plot as a PDF too
    # plt.savefig(f"{plot_filename.split('.')[0]}.pdf")

    # Display the plot
    plt.show()

# Plot and save for encode data
plot_execution_times('execution_times_encode_mrz.csv', 'execution_time_comparison_encode.png', 'encode')

# Plot and save for validate data
plot_execution_times('execution_times_validate_mrz.csv', 'execution_time_comparison_validate.png', 'validate')