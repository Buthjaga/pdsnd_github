from sys import exit
import calendar
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv'}
            #Took out washington because it's missing the Gender and Year columns thus causing errors

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago or new york city). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago', 'new york city']

    while True:
        city = input("For your city, enter 'chicago', or 'new york city'").lower()
        #city is entered here instead of outside the loop coz it will run in infinite loop
        if city in cities:
            print("Thanks for your input")
            break
        else:
            print("Enter a valid city")
    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

    while True:
        month = input("For your month, enter any mohth from 'january' through 'june' or enter 'all'").lower()
        if month in months:
            print("Thanks for your input")
            break
        else:
            print("Enter a valid month")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day_of_week = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("Which day best suits you. You can enter all if that's what you want.").lower()
        if day in day_of_week:
            print("Thanks for your input. Please wait as the data loads.")
            break
        else:
            print("Enter a valid weekday.")
    print('-'*40)
    return city, month, day

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week_name'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    df['start_end_station'] = df['Start Station'] + ' to ' + df['End Station']
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week_name'] == day.title()]

    return df

def choose_interphase(df):
    """Will ask user if they want the first five rows of raw data
    or would they prefer it be broken down by me"""
    while True:
        choice = input("Would you prefer first five rows of raw data? Yes or No ")
        if choice.lower() == 'yes':
            print(df.head())
            exit()
        elif choice.lower() == 'no':
            print("You made a wise choice")
            break

        else:
            print("Enter a valid input")



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    list_of_month = df.groupby(['month'])['month'].count()
    print("The most common month is ", list_of_month.idxmax())

    # TO DO: display the most common day of week
    list_of_day = df.groupby(['day_of_week_name'])['day_of_week_name'].count()
    print("The most common day of week is ", list_of_day.idxmax())

    # TO DO: display the most common start hour
    print("The most common start hour is ", df['hour'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    list_of_start = df.groupby(['Start Station'])['Start Station'].count()
    print("The most commonly used start station is ", list_of_start.idxmax())

    # TO DO: display most commonly used end station
    list_of_end = df.groupby(['End Station'])['End Station'].count()
    print("The most commonly used end station is ", list_of_end.idxmax())

    # TO DO: display most frequent combination of start station and end station trip
    list_of_both = df.groupby(['start_end_station'])['start_end_station'].count()
    print("The most commonly used start and end station is ", list_of_both.idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("The total travel time in hours is ", df['hour'].sum())

    # TO DO: display mean travel time
    print("The average travel time in hours is ", df['hour'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("This is how the user types are grouped by numbers.\n", df.groupby(['User Type'])['User Type'].count())

    # TO DO: Display counts of gender
    print("This is how the male female genders are grouped by numbers.\n", df.groupby(['Gender'])['Gender'].count())

    # TO DO: Display earliest, most recent, and most common year of birth
    print("The earliest year of birth is ", df['Birth Year'].min())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        choose_interphase(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
