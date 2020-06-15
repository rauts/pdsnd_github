import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Please enter the name of the city you would like to explore: ').lower()
        if city in ['chicago', 'new york city', 'washington']:

            break
        else:
            print('Sorry! the input is invalid! Please choose from chicago, new york city or washington')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Enter the name of month to filter the data by "month" or "all" to apply no month filter: ').lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print('Sorry! the input is invalid! Please enter only from january to june')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Enter the name of day of week to filter the data by "day of week" or "all" to apply no day filter: ').lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print('Sorry! the input is invalid! Please choose monday to sunday or all')


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
    df['month'] =  df['Start Time'].dt.month # 1 January-12 December
    df['day_of_week'] = df['Start Time'].dt.weekday_name 
   
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month =  months.index(month) + 1
    
    # filter by month to create the new dataframe
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
    most_common_month = df['month'].mode()[0]
    print(f'Most Common Month: {most_common_month}')
    
    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print(f'Most Common Day of Week: {most_common_day_of_week}')


    # display the most common start hour
    most_common_start_hour = df['Start Time'].dt.hour.mode()[0]
    print(f'Most Common Start Hour: { most_common_start_hour}')


    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    top_start_station = df['Start Station'].value_counts().index[0]
    print('Most Commonly Used Start Station: ', top_start_station)

    # display most commonly used end station
    top_end_station = df['End Station'].value_counts().index[0]
    print('Most Commonly Used End Station: ', top_end_station)

    # display most frequent combination of start station and end station trip
    df['Start-End Station'] = df['Start Station'] + '-' + df['End Station']
    top_startend_station = df['Start-End Station'].value_counts().index[0].split('-')   
    
    print('Most Commonly Used Combination of Start-End Station: \n', top_startend_station)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time: ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:  ', mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

     # Display counts of user types
    user_types_count = df['User Type'].value_counts()
    print('User Type Count \n', user_types_count)
    print()
    # Display counts of gender
    if city != 'washington': # Gender and Birth Year columns are not presented in washington.csv file
        gender_count = df['Gender'].value_counts()
        print('Gender Count\n', gender_count)
        print()
    # Display earliest, most recent, and most common year of birth
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]

        print('Earliest Year of Birth: ', earliest)
        print('Most Recent Year of Birth: ', most_recent)
        print('Most Common Year of Birth: ', most_common)
        print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        
        display_dataset = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        if display_dataset.lower() == 'yes':
        # display 5 rows of the dataset until the user enters no or the rows have reached the end. 
            start_idx = 0
            end_idx   = 5
            while end_idx <= df.shape[0]:                               
                print(df.iloc[start_idx:end_idx])
                display_dataset = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
                if display_dataset.lower() == 'no':
                    break
                else:
                    start_idx = end_idx
                    end_idx   += 5
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
