import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june','july']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze. There are exception statments
    to catch invalid user input that repeats until proper input is provided by the user. 

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\n\nHello! Let\'s explore some US bike share data!')
    city = None
    marker = bool(city in CITY_DATA.items())

    city = input('\nWhat city would you like to see? (Options:New York City,'
    ' Chicago, or Washington) ').lower()
    while city != 'chicago' and city != 'new york city' and city != 'washington':
        print('\nThe options are only Chicago, New York City,\n or Washington, please'
        ' enter one of those locations to continue...\n')
        city = input('\nWhat city would you like to see? ').lower()
    month = input('Which month between January and June? (you can say all!) ').lower()
    while month not in months and month != 'all':
        print('\nThe options are only months between January and June, or you can'
         ' enter ''all'' to see the total data.  Please enter one of these options'
         ' to continue...\n')
        month = input('Which month between January and June? (you can say all!) ').lower()
    day = input('Which day? (you can say all!) ').lower()
    while day not in days and day != 'all':
        print('\nThe options are days of the week (Sunday through Saturday), or you can'
         ' enter ''all'' to see the total data.  Please enter one of these options'
         ' to continue...\n')
        day = input('Which day of the week? (you can say all!) ').lower()

    print('-'*40)
    print('Getting data for the following selected Parameters:'
            '\nCity: {}\nMonth:{}\nDay: {}'.format(city,month,day))

    print('-'*40)
    return city, month, day

def load_data(city,month,day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    This function also adjust month and day columns to adjust for input from the
    main function.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        month = months.index(month) +1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if len(pd.unique(df['month'])) == 1:
        print('Most Common month: Only one month selected')
    else:
        print('Most common month: ',(months[df['month'].value_counts().index[0]-1]).title())

    # display the most common day of week
    if len(pd.unique(df['day_of_week'])) == 1:
        print('Most Common day of the week: Only one day of the week selected.')
    else:
        print('Most common day of the week: ',df['day_of_week'].value_counts().index[0])

    # display the most common start hour
    print('Most common start hour:',(df['Start Time'].dt.hour).value_counts().index[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most common start station: ',df['Start Station'].value_counts().index[0])

    # display most commonly used end station
    print('Most common end station: ',df['End Station'].value_counts().index[0])

    # display most frequent combination of start station and end station trip
    df['start_end'] = '[Start]' + df['Start Station'] + '  &  [End]' + df['End Station']
    print('Most common station combination: ',df['start_end'].value_counts().index[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    sum_travel_time = np.sum(df['Trip Duration'])
    print('Total Trip Duration for Period: ',round(sum_travel_time/60/60,2),'hours')

    # display mean travel time
    mean_travel_time = np.mean(df['Trip Duration'])
    print('Average Trip Duration for Period: ',round(mean_travel_time/60), 'minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Type per ride for Period---','\n',df['User Type'].value_counts())

    # Display counts of gender if data is available
    if 'Gender' in df.columns:
        g_dict = {}
        for marker in df['Gender']:
            g_dict[marker] = g_dict.get(marker,0)+1
        values = g_dict.values()
        g_all = sum(values)
        g_na = g_all - (g_dict['Male']+g_dict['Female'])

        print('\nUser Gender Breakdown by ride---\nMale: {}, {}%\nFemale: {}, {}%\n'
        'Not Reported: {}, {}%'.format(g_dict['Male'],round((g_dict['Male']/g_all)*100,2),
        g_dict['Female'], round((g_dict['Female']/g_all)*100,2), g_na, round((g_na/g_all)*100),2))
    else:
        print('\nGender data is unavailable for this location.')

    # Display earliest, most recent, and most common year of birth if data is available
    if 'Birth Year' in df.columns:
        print('\nUser birth year breakdown by ride---\nEarliest: {}\nMost Recent: {}'
        '\nMost Common: {}'.format(int(df['Birth Year'].min()),int(df['Birth Year'].max()),
        int(df['Birth Year'].mode())))
    else:
        print('Birth Year data is unavailable for this location.')

    print('\n**Please note that these statistics \nare reported by the user'
    ' and may not \nreflect actual user demographics**')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    response = input('Would you like to see 5 rows of the data set? Enter yes or no. ').strip().lower()
    y = 0
    while response == 'yes':
        print(df[y:y+5])
        response = 'no'
        y += 5
        response = input('Would you like to see 5 more rows of the data set? Enter yes or no. ').strip().lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no. \n').strip()
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
