import sys, random, requests, io
from artistNetworks import *
from analyzeNetworks import *
sys.path.append('../Assignment5/')
from fetchArtist import *
from fetchAlbums import *

def get_random_track(album_id):
    url = 'https://api.spotify.com/v1/albums/' + album_id + '/tracks'
    r = requests.get(url)
    assert r.ok, 'no record found'
    dct = r.json()
    assert dct.get('total'), 'no tracks found'
    tracks = [dct['items'][i]['name'] for i in range(len(dct['items']))]
    random_track = random.choice(tracks)
    return random_track

if __name__ == '__main__':
    artists = sys.argv[1:]
    assert artists, 'no artists given'
    artist_ids = [fetchArtistId(x) for x in artists]
    edge_lists = [getEdgeList(x, 2) for x in artist_ids]
    combined = edge_lists[0]
    for i in range(1, len(edge_lists)):
        next_edge_list = edge_lists[i]
        combined = combineEdgeLists(combined, next_edge_list)
    g = pandasToNetworkX(combined)
    
    playlist_artists = []
    playlist_album_ids = []
    for i in range(30):
        albums_exist = False
        artist = randomCentralNode(g)
        while not albums_exist:
            try:
                playlist_album_ids.append(random.choice(fetchAlbumIds(artist)))
                albums_exist = True
            except AssertionError:
                artist = randomCentralNode(g)
        playlist_artists.append(fetchArtistInfo(artist)['name'])

    playlist_albums = []
    playlist_tracks = []
    for album in playlist_album_ids:
        playlist_albums.append(fetchAlbumInfo(album)['name'])
        playlist_tracks.append(get_random_track(album))
    table = zip(playlist_artists, playlist_albums, playlist_tracks)
    with io.open('playlist.csv', 'w', encoding='utf-8') as f:
        f.write(u'artist_name,album_name,track_name\n')
        for x, y, z in table:
            f.write(u'"%s","%s","%s"\n' % (x, y ,z))
