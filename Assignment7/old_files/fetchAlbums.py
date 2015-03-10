import requests
from datetime import datetime

def fetchAlbumIds(artist_id):
    """Using the Spotify API, take an artist ID and 
    returns a list of album IDs in a list
    """
    url = 'https://api.spotify.com/v1/artists/' + artist_id + '/albums?market=US&album_type=album'
    req = requests.get(url)
    assert req.ok, 'No record found.'
    dct = req.json()
    assert dct.get('items'), 'No albums found.'
    return [album['id'] for album in dct['items']]

def fetchAlbumInfo(album_id):
    """Using the Spotify API, take an album ID 
    and return a dictionary with keys 'artist_id', 'album_id' 'name', 'year', popularity'
    """
    url = 'https://api.spotify.com/v1/albums/' + album_id
    req = requests.get(url)
    assert req.ok, 'No record found.'
    dct = req.json()
    album_info = {}
    assert dct.get('name'), 'Album not found'
    album_info['artist_id'] = dct['artists'][0]['id']
    album_info['album_id'] = album_id
    album_info['name'] = dct['name']
    album_info['year'] = dct['release_date'][:4]
    album_info['popularity'] = dct['popularity']
    return album_info

