import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Question 1: Distance Matrix Calculation
def calculate_distance_matrix(df):
    """
        Calculate a distance matrix based on the dataframe, df.
        Args:
            df (pandas.DataFrame): DataFrame containing columns: ID, Start, End, Distance
        Returns:
            pandas.DataFrame: Distance matrix
        """
# Create an empty DataFrame to store the distance matrix
    unique_ids = sorted(set(df['id_start'].unique()) | set(df['id_end'].unique()))
    distance_matrix = pd.DataFrame(np.zeros((len(unique_ids), len(unique_ids))), index=unique_ids, columns=unique_ids)

# Populate the distance matrix
    for index, row in df.iterrows():
        start = row['id_start']
        end = row['id_end']
        distance = row['distance']

# Update distance values in the matrix
        distance_matrix.at[start, end] = distance
        distance_matrix.at[end, start] = distance

# Calculate cumulative distances
    for i in unique_ids:
        for j in unique_ids:
            for k in unique_ids:
                if distance_matrix.at[i, j] == 0 and i != j and i != k and j != k:
                    if distance_matrix.at[i, k] != 0 and distance_matrix.at[k, j] != 0:
                        distance_matrix.at[i, j] = distance_matrix.at[i, k] + distance_matrix.at[k, j]

# Set diagonal values to 0
    np.fill_diagonal(distance_matrix.values, 0)

    return distance_matrix


# Question 2: Unroll Distance Matrix
def unroll_distance_matrix(distance_matrix):
    """
        Unroll a distance matrix to a DataFrame in the style of the initial dataset.
        Args:
            distance_matrix (pandas.DataFrame): Distance matrix generated from calculate_distance_matrix function.
        Returns:
            pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
        """
# Get unique IDs from the distance matrix
    unique_ids = distance_matrix.index

# Create an empty DataFrame to store unrolled data
    unrolled_df = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])

# Generate combinations of IDs and retrieve distances from the matrix
    for i in range(len(unique_ids)):
        for j in range(i + 1, len(unique_ids)):
            id_start = unique_ids[i]
            id_end = unique_ids[j]
            distance = distance_matrix.at[id_start, id_end]

# Append the data to the DataFrame
            unrolled_df = unrolled_df.append({'id_start': id_start, 'id_end': id_end, 'distance': distance},
                                             ignore_index=True)

    return unrolled_df


# Question 3: Finding IDs within Percentage Threshold
def find_ids_within_ten_percentage_threshold(df, reference_id):
    """
       Find all IDs whose average distance lies within 10% of the average distance of the reference ID.
       Args:
           df (pandas.DataFrame): DataFrame containing columns 'id_start', 'id_end', and 'distance'.
           reference_id (int): Reference ID for which the threshold will be calculated.
       Returns:
           pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                             of the reference ID's average distance.
       """
# Calculate average distance for the reference ID
    reference_avg_distance = df[df['id_start'] == reference_id]['distance'].mean()

# Calculate threshold values
    threshold_min = reference_avg_distance - (reference_avg_distance * 0.1)
    threshold_max = reference_avg_distance + (reference_avg_distance * 0.1)

# Filter IDs within the 10% threshold
    filtered_ids = df.groupby('id_start')['distance'].mean().reset_index()
    filtered_ids = filtered_ids[
        (filtered_ids['distance'] >= threshold_min) & (filtered_ids['distance'] <= threshold_max)]

# Sort and return the resulting DataFrame
    result_df = filtered_ids.sort_values(by='id_start')
    return result_df


# Question 4: Calculate Toll Rate
def calculate_toll_rate(df):
    """
        Calculate toll rates for each vehicle type based on the unrolled DataFrame.
        Args:
            df (pandas.DataFrame): DataFrame containing columns 'id_start', 'id_end', 'distance', and 'vehicle_type'
        Returns:
            pandas.DataFrame: DataFrame with added columns for toll rates for each vehicle type
        """
# Define rate coefficients for different vehicle types
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

# Calculate toll rates for each vehicle type based on distance
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient

# Drop the 'distance' column
    df = df.drop(columns='distance')

    return df


# Read the dataset
data = pd.read_csv('dataset-3.csv')

# Calculate distance matrix
resulting_distance_matrix = calculate_distance_matrix(data)
print("Distance Matrix Calculation:\n",resulting_distance_matrix)

# Unroll the distance matrix
unrolled_data = unroll_distance_matrix(resulting_distance_matrix)
print("Unroll Distance Matrix:\n",unrolled_data)

# Find IDs within the 10% threshold of the reference ID
reference_value = 1001404  # Replace with the desired reference ID
resulting_ids_within_threshold = find_ids_within_ten_percentage_threshold(unrolled_data, reference_value)
print("Finding IDs within Percentage Threshold:\n",resulting_ids_within_threshold)

# Calculate toll rates for each vehicle type
result_with_toll_rates = calculate_toll_rate(unrolled_data)
print("Calculate Toll Rate:\n",result_with_toll_rates)