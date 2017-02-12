import os, sys, spotipy
import spotipy.util as util
import time
 
fout = open('playlist.txt', 'w')

artist_uri_list = ['spotify:artist:4dpARuHxo51G3z768sgnrY', 'spotify:artist:6yhD1KjhLxIETFF7vIRf8B', 'spotify:artist:3AVfmawzu83sp94QW7CEGm', 
            'spotify:artist:0du5cEVh5yTK9QJze8zA0C', 'spotify:artist:6aZyMrc4doVtZyKNilOmwu', 'spotify:artist:4gzpq5DPGxSnKTe4SA8HAU', 'spotify:artist:6eUKZXaKkcviH0Ku9w2n3V',
            'spotify:artist:2ysnwxxNtSgbb9t1m2Ur4j', 'spotify:artist:4EzkuveR9pLvDVFNx6foYD', 'spotify:artist:7KMqksf0UMdyA0UCf4R3ux', 'spotify:artist:3LpLGlgRS1IKPPwElnpW35',
            'spotify:artist:1uNFoZAHBGtllmzznpCI3s', 'spotify:artist:6jJ0s89eD6GaHleKKya26X', 'spotify:artist:32WkQRZEVKSzVAAYqukAEA', 'spotify:artist:3yo2YhKm6tyM9NHkd3zgYJ',
            'spotify:artist:04gDigrS5kc9YWfZHwBETP', 'spotify:artist:5Pwc4xIPtQLFEnJriah9YJ', 'spotify:artist:2wY79sveU1sp5g7SokKOiI', 'spotify:artist:1l8Fu6IkuTP0U5QetQJ5Xt',
            'spotify:artist:53XhwfbYqKCa1cC15pYq2q', 'spotify:artist:6JL8zeS1NmiOftqZTRgdTz']
spotify = spotipy.Spotify()

for artist_uri in artist_uri_list:
    top_tracks = spotify.artist_top_tracks(artist_uri)
    artist_name = spotify.artist(artist_uri)['name']
    for track in top_tracks['tracks']:
        fout.write(track['name'] + ' ' + artist_name + '\n')
        print ('writing ' + track['name'] + ' ' + artist_name )

fout.close()
