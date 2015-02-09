import sys
import requests
import csv

def fetchArtistId(name):
    """Using the Spotify API search method, take a string that is the artist's name, 
    and return a Spotify artist ID.
    """
    name = name.lower().replace(' ', '%20')
    url = 'https://api.spotify.com/v1/search?q=' + name + '&type=artist'
    req = requests.get(url)
    assert req.ok, 'No record found.'
    dct = req.json()
    assert dct.get('artists').get('items'), 'Artist not found.'
    return dct['artists']['items'][0]['id']

def fetchArtistInfo(artist_id):
    """Using the Spotify API, takes a string representing the id and
`   returns a dictionary including the keys 'followers', 'genres', 
    'id', 'name', and 'popularity'.
    """
    url = 'https://api.spotify.com/v1/artists/' + artist_id
    req = requests.get(url)
    assert req.ok, 'No record found.'
    dct = req.json()
    artist_info = {}
    assert dct.get('name'), 'Artist not found.'
    artist_info['followers'] = dct['followers']['total']
    artist_info['genres'] = dct['genres']
    artist_info['id'] = artist_id
    artist_info['name'] = dct['name']
    artist_info['popularity'] = dct['popularity']
    return artist_info
