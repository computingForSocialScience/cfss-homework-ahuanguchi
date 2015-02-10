import unicodecsv as csv                # allows access to unicodecsv with the name csv
import matplotlib.pyplot as plt         # allows access to matplotlib.pyplot with the name plt

def getBarChartData():
    f_artists = open('artists.csv')     # opens the file 'artists.csv' in read mode
    f_albums = open('albums.csv')       # opens the file 'albums.csv' in read mode

    artists_rows = csv.reader(f_artists)    # assigns an iterable of rows in f_artists to artist_rows
    albums_rows = csv.reader(f_albums)      # assigns an iterable of rows in f_albums to albums_rows

    artists_header = artists_rows.next()    # takes the first row of artist_rows as the header
    albums_header = albums_rows.next()      # takes the first row of albums_rows as the header

    artist_names = []                   # makes an empty list to be populated later
    
    decades = range(1900,2020, 10)      # makes a list of numbers from 1900 up to and including 2010 with an interval of 10
    decade_dict = {}                    # makes an empty dictionary
    for decade in decades:              # loops over the numbers in the list decades
        decade_dict[decade] = 0         # assigns each decade as a key in decade_dict and sets their initial values to 0
    
    for artist_row in artists_rows:     # loops over each remaining row in artist_rows
        if not artist_row:              # skips to the next row if the row is empty
            continue
        artist_id,name,followers, popularity = artist_row   # assigns each index of artist_row to a variable
        artist_names.append(name)       # takes the name (string at index 1) and adds it to the list artist_names

    for album_row  in albums_rows:      # loops over each remaining row in albums_rows
        if not album_row:               # skips to the next row if the row is empty
            continue
        artist_id, album_id, album_name, year, popularity = album_row   # assigns each index of album_row to a variable
        for decade in decades:              # loops over the numbers in the list decades
            if (int(year) >= int(decade)) and (int(year) < (int(decade) + 10)):
                decade_dict[decade] += 1    # if the album's year (string at index 3 converted to an integer) is between the current and the next decade,
                break                       # increases the album count for the current decade in decade_dict by one and stops looping

    x_values = decades                              # assigns the list decades to the variable x_values
    y_values = [decade_dict[d] for d in decades]    # makes a list containing the count of albums for each decade through a list comprehension
    return x_values, y_values, artist_names         # allows access to the local variables x_values, y_values, and artist_names

def plotBarChart():
    x_vals, y_vals, artist_names = getBarChartData() # calls the above function and assigns its three returned values to variables
    
    fig , ax = plt.subplots(1,1)        # 
    ax.bar(x_vals, y_vals, width=10)    #
    ax.set_xlabel('decades')            #
    ax.set_ylabel('number of albums')   #
    ax.set_title('Totals for ' + ', '.join(artist_names))   #
    plt.show()                          #


    
