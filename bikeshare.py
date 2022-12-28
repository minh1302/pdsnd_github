import time
import pandas as pd
import numpy as np
import helper
from helper import *
# Refactoring 1
# helper.DEBUG_MODE = True
helper.DEBUG_MODE = False

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITY_FILTER_DEFAULT = list(CITY_DATA.keys())[0]
MONTH_FILTER_DEFAULT = "all"
DAY_FILTER_DEFAULT = "all"

CITY_FILTER_OPTIONS = list(CITY_DATA.keys())
TIME_FILTER_OPTIONS = ["month", "day", "both", "none"]
MONTH_FILTER_OPTIONS = [MONTH_FILTER_DEFAULT, 'january', 'february', 'march', 'april', 'may', 'june', 'none']
DAY_FILTER_OPTIONS = [DAY_FILTER_DEFAULT, 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'none']

@print_function 
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city, month, day = (CITY_FILTER_DEFAULT, MONTH_FILTER_DEFAULT, DAY_FILTER_DEFAULT)

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs    
    city = get_input_data(input_questtion = f"Would you like to filter data by city,  please choose your option in : {CITY_FILTER_OPTIONS} \n",                         
                                input_options = CITY_FILTER_OPTIONS)

    # get user input for data filter (month , day, both or none)
    time = get_input_data(input_questtion = f"Would you like to filter data by time,  please choose your option in : {TIME_FILTER_OPTIONS} \n", 
                                input_options = TIME_FILTER_OPTIONS)

    # get user input for month (all, january, february, ... , june)
    if (time in ["month", "both"]):
        month = get_input_data(input_questtion = f"Would you like to filter data by month, please choose your option in : {MONTH_FILTER_OPTIONS} \n", 
                                    input_options = MONTH_FILTER_OPTIONS)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if (time in ["day", "both"]):
        day = get_input_data(input_questtion = f"Would you like to filter data by day, please choose your option in : {DAY_FILTER_OPTIONS} \n", 
                                    input_options = DAY_FILTER_OPTIONS)

    print('-'*40 + "\n")
    return city, month, day

@print_function
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    try:
        # Loading data file into a dataframe.
        df = pd.read_csv(CITY_DATA[city])  

        # Converting the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # Extracting month and day of week from Start Time to create new columns
        df['month'] = df['Start Time'].dt.month

        # Extracting dayofweek from the Start Time column to create a day_of_week column
        df['day_of_week'] = df['Start Time'].dt.dayofweek

        # Extracting hour from the Start Time column to create an hour column
        df['hour'] = df['Start Time'].dt.hour
        
        # Filtering by month if applicable
        if month != MONTH_FILTER_DEFAULT:
            # Useing the index of the months list to get corresponding integer
            month = MONTH_FILTER_OPTIONS.index(month) + 1

            # Filtering by month to create new dataframe
            df = df[df['month'] == month]            
            
        # Filtering by day of week if applicable
        if day != MONTH_FILTER_DEFAULT:
            # Filtering by day of week to create the new dataframe
            df = df[df['day_of_week'] == day.title()]

    except Exception as error:
        print(error)
    finally:
        
        return df

@print_function
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = "NaN"
    most_common_day_of_week = "NaN"
    most_common_start_hour = "NaN"

    try:
        # display the most common month
        most_common_month = MONTH_FILTER_OPTIONS[df['month'].mode()[0]].capitalize()

        # display the most common day of week
        most_common_day_of_week = DAY_FILTER_OPTIONS[df['day_of_week'].mode()[0] + 1].capitalize()

        # display the most common start hour
        most_common_start_hour = df['hour'].mode()[0]

    except Exception as error:
        print(error)
    
    finally:
        print('Most Common Month: ', most_common_month)

        print('Most Common Day Of Week:', most_common_day_of_week)


        print('Most Common Start Hour:', most_common_start_hour)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

@print_function
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()


    most_used_start_station = "NaN"
    most_used_end_station = "NaN"
    most_common_start_end_station = "NaN"

    try:
        # display the most common month
        most_used_start_station = df['Start Station'].mode()[0]

        # display the most common day of week
        most_used_end_station = df['End Station'].mode()[0]

        # display the most common start hour
        most_common_start_end_station = df.groupby(['Start Station', 'End Station']).size().nlargest(1)

    except Exception as error:
        print(error)
    
    finally:
        # display most commonly used start station
        print(f"Most commonly used start station: {most_used_start_station}")   


        # display most commonly used end station
        print(f"Most commonly used end station: {most_used_end_station}")  


        # display most frequent combination of start station and end station trip
        print(f"Most frequent combination of start station and end station trip: \n {most_common_start_end_station}")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

@print_function
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Trip Duration:', df['Trip Duration'].sum())


    # display mean travel time
    print('Mean Trip Duration:', df['Trip Duration'].mean())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

@print_function
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types,'\n')


    # Display counts of gender
    if 'Gender' in df.columns:    
        gender = df['Gender'].value_counts()
        print(gender,'\n')


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Earliest year of Birth:', df['Birth Year'].min())
        print('Most Recent year of Birth:', df['Birth Year'].max())
        most_common_year_of_birth = "nan"
        try:
            most_common_year_of_birth = df['Birth Year'].mode()[0]
        except Exception as error:
            print(error)
        finally:
            print('Most Common year of Birth:', most_common_year_of_birth)   

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
