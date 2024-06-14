from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
from bs4 import BeautifulSoup as bs
import re



load_dotenv()


client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
	auth_string = client_id + ":" + client_secret
	auth_bytes = auth_string.encode("utf-8")
	auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

	url = "https://accounts.spotify.com/api/token"

	headers = {
		"Authorization": "Basic " + auth_base64,
		"Content-Type": "application/x-www-form-urlencoded"
	}

	data = {"grant_type": "client_credentials"}

	result = post(url, headers=headers, data=data)
	json_result = json.loads(result.content)
	token = json_result["access_token"]
	return token

token = get_token()

def get_auth_header(token):
	return {"Authorization": "Bearer " + token}

# Function to get detailed information about an artist
def get_artist_details(token, artist_id):
	url = f"https://api.spotify.com/v1/artists/{artist_id}"
	headers = get_auth_header(token)
	response = get(url, headers=headers)
	return json.loads(response.content)



def get_top_artists(token):
	# Define endpoint for getting playlist data
	
	#top 50 playlist
	playlist_id = '37i9dQZEVXbMDoHDwVN2tF'

	url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

	# Set headers with authorization token
	headers = get_auth_header(token)

	# Get the playlist data
	response = get(url, headers=headers)
	response_json = json.loads(response.content)

	# Initialize an empty list to hold artist information
	artists_info = []

	unique_artists_ids = set()


	# Extract track items from the playlist

	artist_count = 0
	tracks = response_json['tracks']['items']
	for item in tracks:
		# Each track can have multiple artists
		for artist in item['track']['artists']:
			if artist_count >= 7:
				break

			artist_id = artist['id']
			if artist_id in unique_artists_ids:
				continue


			artist_name = artist['name']
			artist_url = artist['external_urls']['spotify']
			
			artist_details = get_artist_details(token, artist_id)
			if artist_details and 'images' in artist_details and artist_details['images']:
				artist_image_url = artist_details['images'][0]['url']
			else:
				artist_image_url = None
			

			# Append artist info to the list
			artists_info.append({
				'id': artist_id,
				'name': artist_name,
				'url': artist_url,
				'image_url': artist_image_url
			})
			
			unique_artists_ids.add(artist_id)
			artist_count += 1

		if artist_count >= 7:
			break


	return artists_info


def get_top_songs(token):
	# Define endpoint for getting playlist data
	
	#top 50 playlist
	playlist_id = '37i9dQZEVXbMDoHDwVN2tF'

	url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

	# Set headers with authorization token
	headers = get_auth_header(token)

	# Get the playlist data
	response = get(url, headers=headers)
	response_json = json.loads(response.content)

	songs_info = []

	# Extract track items from the playlist
	tracks = response_json['tracks']['items']
	for item in tracks[:18]:
		track = item['track']
		song_id = track['id']
		song_name = track['name']
		song_url = track['external_urls']['spotify']
		# album_name = track['album']['name']
		# album_url = track['album']['external_urls']['spotify']


		#artist information
		artist = track['artists'][0]
		artist_name = artist['name']
		artist_url = artist['external_urls']['spotify']

		#Get the image url
		if track['album']['images']:
			image_url = track['album']['images'][0]['url']
		else:
			image_url = None

		# Append song info to the list

		songs_info.append({
			'id': song_id,
			'song_name': song_name,
			'artist_name': artist_name,
			'artist_url': artist_url,
			'song_url': song_url,
			'image_url': image_url
		})

	return songs_info

def get_audio_details(query):

	url = "https://spotify-scraper.p.rapidapi.com/v1/track/download"

	querystring = {"track":query}

	headers = {
		"x-rapidapi-key": "809be7e7bdmsh8717fb81e6217f7p13fb0djsn63369da9510c",
		"x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
	}

	response = get(url, headers=headers, params=querystring)

	audio_details = []

	if response.status_code == 200:
		response_data = response.json()

		if 'youtubeVideo' in response_data and 'audio' in response_data['youtubeVideo']:
			audio_list = response_data['youtubeVideo']['audio']

			if audio_list:
				first_audio_url = audio_list[0]['url']
				duration_text = audio_list[0]['durationText']

				audio_details.append(first_audio_url)
				audio_details.append(duration_text)
			else:
				print("No audio data available")
		else:
			print("No 'youtubeVideo' or 'audio' data found")
	else:
		print("Failed to get data")	
	
	return audio_details


def music(request, pk):

	track_id = pk

	url = "https://spotify-scraper.p.rapidapi.com/v1/track/metadata"

	querystring = {"trackId":track_id}

	headers = {
		"x-rapidapi-key": "809be7e7bdmsh8717fb81e6217f7p13fb0djsn63369da9510c",
		"x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
	}

	response = get(url, headers=headers, params=querystring)

	if response.status_code == 200:
		data = response.json()
		# track_name, artist_name


		track_name = data.get("name")
		artists_list = data.get("artists", [])
	
		track_image1 = data.get("album", {}).get("cover", [])[2].get("url")


		first_artist_name = artists_list[0].get("name") if artists_list else "No artist found"

		audio_details_query = track_name + first_artist_name
		audio_details = get_audio_details(audio_details_query)
		audio_url = audio_details[0]
		duration_text = audio_details[1]

		context = {
			'track_name' : track_name,
			'artist_name' : first_artist_name,
			'audio_url': audio_url,
			'duration_text': duration_text,
			'track_image': track_image1,
		}
		
	
	return render(request, 'music.html', context)




@login_required(login_url='login')
def index(request):
	artists_info = get_top_artists(token)
	top_track_list = get_top_songs(token)

	# Divide the list into three parts
	first_six_tracks = top_track_list[:6]
	second_six_tracks = top_track_list[6:12]
	third_six_tracks = top_track_list[12:18]
	

	# print(top_track_list)
	context = {
		'artists_info' : artists_info,
		'first_six_tracks' : first_six_tracks,
		'second_six_tracks' : second_six_tracks,
		'third_six_tracks' : third_six_tracks,
	}

	return render(request, 'index.html', context)


def search(request):
	if request.method == 'POST':
		search_query = request.POST['search_query']

		url = "https://spotify-scraper.p.rapidapi.com/v1/search"

		querystring = {"term":search_query,"type":"track"}

		headers = {
			"x-rapidapi-key": "809be7e7bdmsh8717fb81e6217f7p13fb0djsn63369da9510c",
			"x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
		}

		response = get(url, headers=headers, params=querystring)

		track_list = []

		if response.status_code == 200:
			data = response.json()

			search_results_count = data["tracks"]["totalCount"]

			tracks = data["tracks"]["items"]

			for track in tracks:
				track_name = track["name"]
				artist_name = track["artists"][0]["name"]
				duration = track["durationText"]
				trackid = track["id"]
				track_image = track["album"]["cover"][2]["url"]#Change if needed

				track_list.append({
					'track_name': track_name,
					'artist_name': artist_name,
					'duration' : duration,
					'trackid': trackid,
					'track_image': track_image
				})

		context ={
			'search_results_count': search_results_count,
			'track_list': track_list,
		}
		return render(request, 'search.html', context)
	else:
		return render(request, 'search.html', context)


def profile(request, pk):

	artist_id = pk

	url = "https://spotify-scraper.p.rapidapi.com/v1/artist/overview"

	querystring = {"artistId": artist_id}

	headers = {
		"x-rapidapi-key": "809be7e7bdmsh8717fb81e6217f7p13fb0djsn63369da9510c",
		"x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
	}

	response = get(url, headers=headers, params=querystring)

	if response.status_code == 200:
		data = response.json()

		name = data["name"]
		monthly_listeners = data["stats"]["monthlyListeners"]
		header_url = data["visuals"]["header"][0]["url"]


		top_tracks= []

		for track in data["discography"]["topTracks"]:
			trackid = str(track["id"])
			trackname = str(track["name"])
			track_image = track["album"]["cover"][2]["url"]


			track_info = {
				"id": track["id"],
				"name": track["name"],
				"durationText": track["durationText"],
				"playCount": track["playCount"],
				"track_image": track_image
				
			}

			top_tracks.append(track_info)

		artist_data = {
			'name': name,
			'monthlyListeners': monthly_listeners,
			'headerUrl': header_url,
			'topTracks': top_tracks,
		}

	else:
		artist_data = {}

	return render(request, 'profile.html', artist_data)




def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = auth.authenticate(username=username, password=password)

		if user is not None:
			auth.login(request, user)
			return redirect('/')
		else:
			messages.info(request, 'Invalid credentials')
			return redirect('login')
	
	return render(request, 'login.html')

def signup(request):
	if request.method == 'POST':
		email = request.POST['email']
		username = request.POST['username']
		password = request.POST['password']
		password2 = request.POST['password2']
		
		if password == password2:
			if User.objects.filter(email=email).exists():
				messages.info(request, 'Email already exists')
				return redirect('signup')
			elif User.objects.filter(username=username).exists():
				messages.info(request, 'Username already exists')
				return redirect('signup')
			else:
				user = User.objects.create_user(username=username, email=email, password=password)
				user.save()
				
				#login user
				user_login = auth.authenticate(username=username, password=password)
				auth.login(request, user_login)
				return redirect('/')
				
				
		else:
			messages.info(request, 'Passwords do not match')
			return redirect('signup')
			

	else:
		return render(request, 'signup.html')


@login_required(login_url='login')
def logout(request):
	auth.logout(request)
	return redirect('login')

