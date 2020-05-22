import time
import pandas as pd
import numpy as np
import datetime as dt
import click

cities = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

mnths = ('january', 'february', 'march', 'april', 'may', 'june')

wkday = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday')


def option(prmpt, options=('y', 'n')):
    """Return a valid input from the user given an array of possible answers.
    """

    while True:
        option = input(prmpt).lower().strip()
        # terminate the program if the input is end
        if option == 'end':
            raise SystemExit
        # triggers if the input has only one name
        elif ',' not in option:
            if option in options:
                break
        # triggers if the input has more than one name
        elif ',' in option:
            option = [i.strip().lower() for i in option.split(',')]
            if list(filter(lambda x: x in options, option)) == option:
                break

        prmpt = ("\nSomething is not right. Please mind the formatting and "
                  "be sure to enter a valid option:\n>")

    return option


def obtain_filters():
    """Ask user to specify city(ies) and filters, month(s) and weekday(s).
    Returns:
        (str) city -name of the city(ies) to analyze
        (str) month -name of the month(s) to filter
        (str) day -name of the day(s) of week to filter
    """

    print("\n\nLet's explore some US bikeshare data!\n")

    print("Type end at any time if you would like to exit the program.\n")

    while True:
        cty = option("\nFor what city(ies) do you want do select data, "
                      "New York City, Chicago or Washington? Use commas "
                      "to list the names.\n>", cities.keys())
        mnth = option("\nFrom January to June, for what month(s) do you "
                       "want do filter data? Use commas to list the names.\n>",
                       mnths)
        dy = option("\nFor what weekday(s) do you want do filter bikeshare "
                     "data? Use commas to list the names.\n>", wkday)

        # confirm the user input
        confirmatn = option("\nPlease confirm that you would like to apply "
                              "the following filter(s) to the bikeshare data."
                              "\n\n City(ies): {}\n Month(s): {}\n Weekday(s)"
                              ": {}\n\n [y] Yes\n [n] No\n\n>"
                              .format(cty, mnth, dy))
        if confirmatn == 'y':
            break
        else:
            print("\nLet's try this again!")

    print('-'*40)
    return cty, mnth, dy


def data_to_load(cty, mnth, dy):
    """Load data for the specified filters of city(ies), month(s) and
       day(s) whenever applicable.
    Args:
        (str) city - name of the city(ies) to analyze
        (str) month - name of the month(s) to filter
        (str) day - name of the day(s) of week to filter
    Returns:
        df - Pandas DataFrame containing filtered data
    """

    print("\nThe program is loading the data for the filters of your option.")
    start_time = time.time()

    # filter the data according to the selected city filters
    if isinstance(cty, list):
        df = pd.concat(map(lambda cty: pd.read_csv(cities[cty]), cty),
                       sort=True)
        # reorganize DataFrame columns after a city concat
        try:
            df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time',
                                     'Trip Duration', 'Start Station',
                                     'End Station', 'User Type', 'Gender',
                                     'Birth Year'])
        except:
            pass
    else:
        df = pd.read_csv(cities[cty])

    # create columns to display statistics
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour

    # filter the data according to month and weekday into two new DataFrames
    if isinstance(mnth, list):
        df = pd.concat(map(lambda mnth: df[df['Month'] ==
                           (mnths.index(mnth)+1)], mnth))
    else:
        df = df[df['Month'] == (mnths.index(mnth)+1)]

    if isinstance(dy, list):
        df = pd.concat(map(lambda dy: df[df['Weekday'] ==
                           (dy.title())], dy))
    else:
        df = df[df['Weekday'] == dy.title()]

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)

    return df


def time_statistics(df):
    """Display statistics on the most frequent times of travel."""

    print('\nDisplaying the statistics on the most frequent times of '
          'travel...\n')
    starttime = time.time()

    # display the most common month
    most_comm_mnth = df['Month'].mode()[0]
    print('For the selected filter, the month with the most travels is: ' +
          str(mnths[most_comm_mnth-1]).title() + '.')

    # display the most common day of week
    most_comm_dy = df['Weekday'].mode()[0]
    print('For the selected filter, the most common day of the week is: ' +
          str(most_comm_dy) + '.')

    # display the most common start hour
    most_comm_hr = df['Start Hour'].mode()[0]
    print('For the selected filter, the most common start hour is: ' +
          str(most_comm_hr) + '.')

    print("\nThis took {} seconds.".format((time.time() - starttime)))
    print('-'*40)


def station_statistics(df):
    """Display statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    starttime = time.time()

    # display most commonly used start station
    most_comm_startstn = str(df['Start Station'].mode()[0])
    print("For the selected filters, the most common start station is: " +
          most_comm_startstn)

    # display most commonly used end station
    most_comm_endstn = str(df['End Station'].mode()[0])
    print("For the selected filters, the most common start end is: " +
          most_comm_endstn)

    # display most frequent combination of start station and
    # end station trip
    df['Start-End Combination'] = (df['Start Station'] + ' - ' +
                                   df['End Station'])
    most_common_start_end_combination = str(df['Start-End Combination']
                                            .mode()[0])
    print("For the selected filters, the most common start-end combination "
          "of stations is: " + most_common_start_end_combination)

    print("\nThis took {} seconds.".format((time.time() - starttime)))
    print('-'*40)


def tripDuration_statistics(df):
    """Display statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    starttime = time.time()

    # display total travel time
    tot_traveltime = df['Trip Duration'].sum()
    tot_traveltime = (str(int(tot_traveltime//86400)) +
                         'd ' +
                         str(int((tot_traveltime % 86400)//3600)) +
                         'h ' +
                         str(int(((tot_traveltime % 86400) % 3600)//60)) +
                         'm ' +
                         str(int(((tot_traveltime % 86400) % 3600) % 60)) +
                         's')
    print('For the selected filters, the total travel time is : ' +
          tot_traveltime + '.')

    # display mean travel time
    mn_traveltime = df['Trip Duration'].mean()
    mn_traveltime = (str(int(mn_traveltime//60)) + 'm ' +
                        str(int(mn_traveltime % 60)) + 's')
    print("For the selected filters, the mean travel time is : " +
          mn_traveltime + ".")

    print("\nThis took {} seconds.".format((time.time() - starttime)))
    print('-'*40)


def user_statistics(df, cty):
    """Display statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    starttime = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_string()
    print("Distribution for user types:")
    print(user_types)

    # Display counts of gender
    try:
        gender_distbn = df['Gender'].value_counts().to_string()
        print("\nDistribution for each gender:")
        print(gender_distbn)
    except KeyError:
        print("We're sorry! There is no data of user genders for {}."
              .format(cty.title()))

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birthyr = str(int(df['Birth Year'].min()))
        print("\nFor the selected filter, the oldest person to ride one "
              "bike was born in: " + earliest_birthyr)
        mst_recent_birthyr = str(int(df['Birth Year'].max()))
        print("For the selected filter, the youngest person to ride one "
              "bike was born in: " + mst_recent_birthyr)
        mst_comm_birthyr = str(int(df['Birth Year'].mode()[0]))
        print("For the selected filter, the most common birth year amongst "
              "riders is: " + mst_comm_birthyr)
    except:
        print("We're sorry! There is no data of birth year for {}."
              .format(cty.title()))

    print("\nThis took {} seconds.".format((time.time() - starttime)))
    print('-'*40)


def rawData(df, mrk_place):
    """Display 5 line sorted raw data each time."""

    print("\nYou opted to view raw data.")

    # this variable holds where the user last stopped
    if mrk_place > 0:
        last_place = option("\nWould you like to continue from where you "
                            "stopped time? \n [y] Yes\n [n] No\n\n>")
        if last_place == 'n':
            mrk_place = 0

    # sort data by column
    if mrk_place == 0:
        sort_df = option("\nHow like to sort the way the data is "
                         "displayed in the dataframe? Hit Enter to view "
                         "unsorted.\n \n [st] Start Time\n [et] End Time\n "
                         "[td] Trip Duration\n [ss] Start Station\n "
                         "[es] End Station\n\n>",
                         ('st', 'et', 'td', 'ss', 'es', ''))

        asc_or_dsc = option("\nWould you like it to be sorted ascending or "
                             "descending? \n [a] Ascending\n [d] Descending"
                             "\n\n>",
                             ('a', 'd'))

        if asc_or_dsc == 'a':
            asc_or_dsc = True
        elif asc_or_dsc == 'd':
            asc_or_dsc = False

        if sort_df == 'st':
            df = df.sort_values(['Start Time'], ascending=asc_or_dsc)
        elif sort_df == 'et':
            df = df.sort_values(['End Time'], ascending=asc_or_dsc)
        elif sort_df == 'td':
            df = df.sort_values(['Trip Duration'], ascending=asc_or_dsc)
        elif sort_df == 'ss':
            df = df.sort_values(['Start Station'], ascending=asc_or_dsc)
        elif sort_df == 'es':
            df = df.sort_values(['End Station'], ascending=asc_or_dsc)
        elif sort_df == '':
            pass

    # each loop displays 5 lines of raw data
    while True:
        for i in range(mrk_place, len(df.index)):
            print("\n")
            print(df.iloc[mrk_place:mrk_place+5].to_string())
            print("\n")
            mrk_place += 5

            if option("Do you want to keep printing raw data?"
                      "\n\n[y]Yes\n[n]No\n\n>") == 'y':
                continue
            else:
                break
        break

    return mrk_place


def main():
    while True:
        click.clear()
        cty, mnth, dy = obtain_filters()
        df = data_to_load(cty, mnth, dy)

        mrk_place = 0
        while True:
            selectData = option("\nPlease select the information you would "
                                 "like to obtain.\n\n [ts] Time Stats\n [ss] "
                                 "Station Stats\n [tds] Trip Duration Stats\n "
                                 "[us] User Stats\n [rd] Display Raw Data\n "
                                 "[r] Restart\n\n>",
                                 ('ts', 'ss', 'tds', 'us', 'rd', 'r'))
            click.clear()
            if selectData == 'ts':
                time_statistics(df)
            elif selectData == 'ss':
                station_statistics(df)
            elif selectData == 'tds':
                tripDuration_statistics(df)
            elif selectData == 'us':
                user_statistics(df, cty)
            elif selectData == 'rd':
                mrk_place = rawData(df, mrk_place)
            elif selectData == 'r':
                break

        restrt = option("\nWould you like to restart?\n\n[y]Yes\n[n]No\n\n>")
        if restrt.lower() != 'y':
            break


if __name__ == "__main__":
    main()
