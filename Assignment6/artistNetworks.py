import requests

def getRelatedArtists(artistID):
    url = 'https://api.spotify.com/v1/artists/' + artistID + '/related-artists'
    r = requests.get(url)
    assert r.ok, 'no record found'
    dct = r.json()
    assert dct.get('artists'), 'artists not found'
    artists_dct = dct['artists']
    related_artists = [x['id'] for x in artists_dct]
    return related_artists

def getDepthEdges(artistID, depth):
    pairs = [(artistID, x) for x in getRelatedArtists(artistID)]    # depth 1        
    for i in range(depth - 1):
        new_pairs = []
        for pair in pairs:
            artist = pair[1]
            current_pairs = set(pairs + new_pairs)
            new_pairs += [(artist, x) for x in getRelatedArtists(artist)
                          if (artist, x) not in current_pairs
                          and (x, artist) not in current_pairs]
        pairs += new_pairs
    return pairs
