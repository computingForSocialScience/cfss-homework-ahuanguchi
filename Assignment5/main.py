import sys
from fetchArtist import fetchArtistId, fetchArtistInfo
from fetchAlbums import fetchAlbumIds, fetchAlbumInfo
from csvUtils import writeArtistsTable, writeAlbumsTable
from barChart import plotBarChart

# Where the main.py script says # YOUR CODE HERE, you should write code using the imported functions which:

# Loops through the list of artist names, gets their IDs and corresponding info (using fetchArtistId() and fetchArtistInfo()).
# Loops through the artist IDs and gets their album IDs and album info (using fetchAlbumIds() and fetchAlbumInfo()).
# Writes out CSV files given these lists of artist info dictionaries and album info dictionaries (using writeArtistsTable() and writeAlbumsTable().
# Calls plotBarChart() to read and plot your CSV files.

if __name__ == '__main__':
    artist_names = sys.argv[1:]
    print "input artists are ", artist_names
    # YOUR CODE HERE
    all_artists = []
    all_albums = []
    for artist in artist_names:
        artist_id = fetchArtistId(artist)
        artist_info = fetchArtistInfo(artist_id)
        all_artists.append(artist_info)
        album_ids = fetchAlbumIds(artist_id)
        albums_info = [fetchAlbumInfo(x) for x in album_ids]
        all_albums += albums_info
    writeArtistsTable(all_artists)
    writeAlbumsTable(all_albums)
    plotBarChart()
