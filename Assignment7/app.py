from flask import Flask, render_template, request, redirect, url_for
import pymysql, sys
sys.path.append('old_files/')
from artistNetworks import *
from analyzeNetworks import *
from fetchArtist import *
from fetchAlbums import *
from makePlaylist import *

dbname = "playlists"
host = "localhost"
user = "root"
passwd = ""
db = pymysql.connect(db=dbname, host=host, user=user, passwd=passwd, charset='utf8')
c = db.cursor()

app = Flask(__name__)

def createNewPlaylist(root_artist):
    c.execute("""
        CREATE TABLE IF NOT EXISTS playlists (
            id INT PRIMARY KEY AUTO_INCREMENT,
            rootArtist VARCHAR(255) CHARACTER SET utf8
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            playlistId INT,
            songOrder INT,
            artistName VARCHAR(255) CHARACTER SET utf8,
            albumName VARCHAR(255) CHARACTER SET utf8,
            trackName VARCHAR(255) CHARACTER SET utf8
        );
    """)
    c.execute("""
        SELECT id FROM playlists
        ORDER BY id DESC LIMIT 1;
    """)
    last_id = c.fetchone()
    playlist_id = (last_id[0] + 1) if last_id else 1
    c.execute(
        "INSERT INTO playlists VALUES (%s, %s);",
        (playlist_id, root_artist)
    )
    
    artist_id = fetchArtistId(root_artist)
    edge_list = getEdgeList(artist_id, 2)
    g = pandasToNetworkX(edge_list)
    
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
    
    
    playlist_id_col = [playlist_id] * 30
    song_order = [x for x in range(1, 31)]
    songs_table = zip(
        playlist_id_col,
        song_order,
        playlist_artists,
        playlist_albums,
        playlist_tracks
    )
    c.executemany(
        "INSERT INTO songs VALUES (%s, %s, %s, %s, %s);",
        songs_table
    )
    db.commit()

@app.route('/')
def make_index_resp():
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/
    
    return(render_template('index.html'))


@app.route('/playlists/')
def make_playlists_resp():
    c.execute("""
        SELECT * FROM playlists;
    """)
    playlists = c.fetchall()
    return render_template('playlists.html', playlists=playlists)


@app.route('/playlist/<playlistId>')
def make_playlist_resp(playlistId):
    return render_template('playlist.html', songs=songs)


@app.route('/addPlaylist/', methods=['GET','POST'])
def add_playlist():
    if request.method == 'GET':
        # This code executes when someone visits the page.
        return(render_template('addPlaylist.html'))
    elif request.method == 'POST':
        # this code executes when someone fills out the form
        artistName = request.form['artistName']
        # YOUR CODE HERE
        return(redirect("/playlists/"))



if __name__ == '__main__':
    # createNewPlaylist('of Montreal')
    # createNewPlaylist('Deerhoof')
    
    app.debug = True
    app.run()
