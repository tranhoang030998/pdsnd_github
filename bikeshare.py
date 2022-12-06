import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    global city,month,day
    month = "all"
    month_all = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    day = "all"
    day_all = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    citys = ['chicago', 'new york', 'washington']
    modes = ['month', 'day', 'both', 'none']
   
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data of Chicago, New York, or Washington ?\n').lower()
        if city not in citys:
            print("Invalid Input. Please try again")
        else:
            break
            
    while True:
        mode = input('Would you like to filter the data by month, day or both? \nPlease type "month", "day", "both"? Type \"none\" for no filter:\n').lower()
        if mode not in modes:
            print("Invalid Input. Please try again")
        else:
            break
                    
    
    # get user input for month (all, january, february, ... , june)
    if mode == 'both' or mode == 'month':
        while True:
            month = input('Which month between January and June do you like to see the data or all ?\n').lower()
            if month not in month_all:
                print("Invalid Input. Please try again")
            else:
                break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if mode == 'both' or mode == 'day':
        while True:
            day = input('Which day do you like to see the data or all ?\n').lower()
            if day not in day_all:
                print("Invalid Input. Please try again")
            else:
                break

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
    df = pd.read_csv(CITY_DATA[city])

    # convert the type of Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Create new columns by extract month day of the week from Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most common month is: ',df['month'].value_counts().idxmax())
    print('Count: ',df['month'].value_counts().max())

    # display the most common day of week
    print('Most common day of week is: ',df['day_of_week'].value_counts().idxmax())
    print('Count: ',df['day_of_week'].value_counts().max())

    # display the most common start hour
    print('Most common hour is: ',df['Start Time'].dt.hour.value_counts().idxmax())
    print('Count: ',df['Start Time'].dt.hour.value_counts().max())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most common start station is: ',df['Start Station'].value_counts().idxmax())
    print('Count: ',df['Start Station'].value_counts().max())

    # display most commonly used end station
    print('Most common end station is: ',df['End Station'].value_counts().idxmax())
    print('Count: ',df['End Station'].value_counts().max())

    # display most frequent combination of start station and end station trip
    df['Start End Station'] = df[["Start Station", "End Station"]].apply(" - ".join, axis=1)
    print('Most common used start and end station is: ',df['Start End Station'].value_counts().idxmax())
    print('Count: ',df['Start End Station'].value_counts().max())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time is: ',df['Trip Duration'].sum())

    # display mean travel time
    print('Average travel time is: ',df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    for idx, user_type in enumerate(df["User Type"].value_counts().index.tolist()):
        print('User type is: ', user_type)
        print('Count:', df["User Type"].value_counts()[idx])
        
        # Display counts of gender
    if 'Gender' not in df.columns:
        print('No gender\'s information')
    else:
        for idx, gender in enumerate(df["Gender"].value_counts().index.tolist()):
            print('Gender is: ', gender)
            print('Count:', df["Gender"].value_counts()[idx])

        # Display earliest, most recent, and most common year of birth
        print('The most earliest year of birth is: ',df['Birth Year'].min())

        print('The most recent year of birth is: ',df['Birth Year'].max())

        print('The most common year of birth is: ',df['Birth Year'].value_counts().idxmax())
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Display data
# Meet the requirement
def display_data(df):    
    start_loc = 0
    view_data = 'False'
    while view_data == 'False':
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
        if view_data == 'yes':
            start_loc += 5
            print(df.head(start_loc))       
            view_data = 'False'
        else:
            break
    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

            
if __name__ == "__main__":
	main()

