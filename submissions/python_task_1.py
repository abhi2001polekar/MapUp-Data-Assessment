import pandas as pd
import numpy as np

def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here

    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    np.fill_diagonal(car_matrix.values, 0)

    return car_matrix



def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    a = [] 

    for row in df['car']: 
        if row <= 15 : 
            a.append('low') 
        elif row > 15 and row <=25: 
            a.append('medium') 
        else: 
            a.append('high')

    df['car_type']=a

    return df.value_counts("car_type").to_dict()


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here

    return df.index[df['bus'] > np.mean(df['bus'])*2 ].tolist()


def filter_routes(df1)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    average_truck_per_route = df.groupby('route')['truck'].mean()

    filtered_routes = average_truck_per_route[average_truck_per_route > 7]

    sorted_routes = filtered_routes.sort_values(ascending=True).index.to_list()
    return sorted_routes


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here


    matrix = matrix.map(lambda x: x * 0.75 if int(x) > 20 else x * 1.25)

    # Round the modified values to 1 decimal place
    matrix = matrix.round(1)
    return matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period
    Args:
        df (pandas.DataFrame)
    Returns:
        pd.Series: return a boolean series
    """
    # Combine 'startDay' and 'startTime' columns into a single datetime column 'start_datetime'
    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'],errors='coerce')

    # Combine 'endDay' and 'endTime' columns into a single datetime column 'end_datetime'
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'],errors='coerce')

    # Calculate the duration of each timestamp
    df['duration'] = df['end_datetime'] - df['start_datetime']

    # Check if the duration covers a full 24-hour period and spans all 7 days of the week
    full_24_hour = df['duration'].dt.total_seconds() >= 86400  # 24 hours in seconds
    all_7_days = df['start_datetime'].dt.dayofweek.nunique() == 7

    # Aggregate results based on ('id', 'id_2') pairs
    df = df.groupby(['id', 'id_2']).apply(lambda x: all(full_24_hour.loc[x.index]) and all_7_days.loc[x.index[0]])
    return df


df = pd.read_csv('dataset-1.csv')
print(get_type_count(df))
print(generate_car_matrix(df))
print(get_bus_indexes(df))
print(filter_routes(df))
print(multiply_matrix(generate_car_matrix(df)))
df2 = pd.read_csv('dataset-2.csv')
print(time_check(df2))
