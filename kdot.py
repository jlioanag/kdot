import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import plotly.graph_objects as go
import plotly.io as pio

kdot_uri = 'spotify:artist:2YZyLoL8N0Wb9xBt1NhZWg'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results = spotify.artist_albums(kdot_uri, album_type='album')
raw_albums = results['items']
while results['next']:
	results = spotify.next(results)
	raw_albums.extend(results['items'])

album_names = []

for album in raw_albums:
	album_names.append(album['name'])

album_names = list(dict.fromkeys(album_names))
album_names.remove('DAMN. COLLECTORS EDITION.')
album_names.remove('good kid, m.A.A.d city (Deluxe)')

albums = []

for album in raw_albums:
	if album['name'] in album_names or len(albums) <= 0:
		album_names.remove(album['name'])
		albums.append(album)

features = ['valence', 'danceability', 'energy', 'speechiness']

for feature in features:

	fig = go.Figure()

	for album in albums:
		album_uri = album['uri']

		results = spotify.album_tracks(str(album_uri), limit=50, offset=0)
		tracks = results['items']
		while results['next']:
			results = spotify.next(results)
			tracks.extend(results['items'])

		track_uris = []
		track_names = []
		for track in tracks:
			track_names.append(track['name'])
			track_uris.append(track['uri'])

		results = spotify.audio_features(tracks=track_uris)

		feature_list = []

		for track in results:
			feature_list.append(track[feature])

		fig.add_trace(go.Scatter(x=track_names, y=feature_list,
						mode='markers',
						name=album['name']))
	fig.update_layout(title_text=feature)
	fig.update_xaxes(showticklabels=False)
	filename = 'data/' + feature + '.html'
	pio.write_html(fig, file=filename, auto_open=False)