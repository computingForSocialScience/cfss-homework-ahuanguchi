from io import open

def writeArtistsTable(artist_info_list):
    """Given a list of dictionries, each as returned from 
    fetchArtistInfo(), write a csv file 'artists.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY
    """
    f = open('artists.csv', 'w')
    try:
        f.write(u'ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY\n')
        for artist_info in artist_info_list:
            artist_id = artist_info['id']
            name = artist_info['name']
            followers = artist_info['followers']
            popularity = artist_info['popularity']
            f.write(u'%s,"%s",%s,%s\n' % (artist_id, name, followers, popularity))
    finally:
        f.close()
      
def writeAlbumsTable(album_info_list):
    """
    Given list of dictionaries, each as returned
    from the function fetchAlbumInfo(), write a csv file
    'albums.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY
    """
    f = open('albums.csv', 'w')
    try:
        f.write(u'ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY')
        for album_info in album_info_list:
            artist_id = album_info['artist_id']
            album_id = album_info['album_id']
            name = album_info['name']
            year = album_info['year']
            popularity = album_info['popularity']
            f.write(u'%s,%s,"%s",%s,%s' % (artist_id, album_id, name, year, popularity))
    finally:
        f.close()
        
