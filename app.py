from flask import Flask, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
import unittest
from app import app, db, Playlist, Song

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_show_all_playlists(self):
        """Test whether the endpoint '/playlists' returns a status code 200, indicating success."""
        response = self.app.get("/playlists")
        self.assertEqual(response.status_code, 200)

    def test_show_playlist(self):
        """Test whether a specific playlist detail page is returned successfully."""
        playlist = Playlist(name="Test Playlist", description="Test Description")
        db.session.add(playlist)
        db.session.commit()

        response = self.app.get(f"/playlists/{playlist.id}")
        self.assertEqual(response.status_code, 200)

    def test_add_playlist(self):
        """Test whether a new playlist can be added successfully."""
        response = self.app.post("/playlists/add", data={"name": "New Playlist", "description": "New Description"})
        self.assertEqual(response.status_code, 302)  # Redirects to /playlists after adding playlist

    def test_show_all_songs(self):
        """Test whether the endpoint '/songs' returns a status code 200, indicating success."""
        response = self.app.get("/songs")
        self.assertEqual(response.status_code, 200)

    def test_show_song(self):
        """Test whether a specific song detail page is returned successfully."""
        song = Song(title="Test Song", artist="Test Artist")
        db.session.add(song)
        db.session.commit()

        response = self.app.get(f"/songs/{song.id}")
        self.assertEqual(response.status_code, 200)

    def test_add_song(self):
        """Test whether a new song can be added successfully."""
        response = self.app.post("/songs/add", data={"title": "New Song", "artist": "New Artist"})
        self.assertEqual(response.status_code, 302)  # Redirects to /songs after adding song

    def test_add_song_to_playlist(self):
        """Test whether a song can be added to a playlist successfully."""
        playlist = Playlist(name="Test Playlist", description="Test Description")
        db.session.add(playlist)
        db.session.commit()

        response = self.app.post(f"/playlists/{playlist.id}/add-song", data={"song": 1})
        self.assertEqual(response.status_code, 302)  # Redirects to /playlists/{playlist_id} after adding song to playlist

@app.route("/")
def root():
    """Homepage: redirect to /playlists."""
    return redirect("/playlists")

##############################################################################
# Playlist routes

@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""
    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)

@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""
    playlist = Playlist.query.get_or_404(playlist_id)
    songs = playlist.songs
    return render_template("playlist_detail.html", playlist=playlist, songs=songs)

@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle add-playlist form."""
    form = PlaylistForm()
    if form.validate_on_submit():
        new_playlist = Playlist(name=form.name.data, description=form.description.data)
        db.session.add(new_playlist)
        db.session.commit()
        return redirect("/playlists")
    return render_template("add_playlist.html", form=form)

##############################################################################
# Song routes

@app.route("/songs")
def show_all_songs():
    """Show list of songs."""
    songs = Song.query.all()
    return render_template("songs.html", songs=songs)

@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """Return a specific song."""
    song = Song.query.get_or_404(song_id)
    return render_template("song_detail.html", song=song)

@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Handle add-song form."""
    form = SongForm()
    if form.validate_on_submit():
        new_song = Song(title=form.title.data, artist=form.artist.data)
        db.session.add(new_song)
        db.session.commit()
        return redirect("/songs")
    return render_template("add_song.html", form=form)

@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a playlist and redirect to list."""
    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()
    curr_on_playlist = [s.id for s in playlist.songs]
    form.song.choices = (db.session.query(Song.id, Song.title)
                          .filter(Song.id.notin_(curr_on_playlist))
                          .all())
    if form.validate_on_submit():
        playlist_song = PlaylistSong(song_id=form.song.data, playlist_id=playlist_id)
        db.session.add(playlist_song)
        db.session.commit()
        return redirect(f"/playlists/{playlist_id}")
    return render_template("add_song_to_playlist.html", playlist=playlist, form=form)

if __name__ == '__main__':
    unittest.main()
