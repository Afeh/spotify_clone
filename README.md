## Spotify Clone

This project is a full-fledged Spotify clone web application built with Django, designed to provide a rich music streaming experience. It seamlessly integrates the official Spotify API for core functionalities like user authentication,and music playback control. Additionally, it utilizes Rapid API's spotify-scraper API to enhance functionality by fetching supplementary data that might not be readily available through the official API.


## Key Features:

- User Authentication: Securely log in and manage user accounts.
- Music Streaming: Play, pause, skip, and control music playback using the official Spotify API.
- Data Enrichment (Optional): Utilize Rapid API's spotify-scraper API to potentially access additional music data not exposed by the official API (subject to Rapid API's terms and scraper availability).



## How to use
1. Fork the repo
2. Clone the repo
3. Intall dependencies

- Install Python 3.12.2
```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.12.2
```
- Install Python 3.12-venv
```bash
sudo apt install python3.12-venv
```
- Create Virtual Environment
```bash
cd authapp
python3.12 -m venv venv
```
- Activate Virtual Environment
```bash
source venv/bin/activate
```
- Install Requirements
```bash
pip install -r requirements.txt
```
- Run Migrations
```bash
python manage.py migrate
```
- Run Server
```bash
python manage.py runserver
```
4. Go to [http://localhost:8000](http://localhost:8000) to see the project running.

If you like this project, please give it a star ⭐️


## Acknowledgement

Built by [Afebu Balogun](https://twitter.com/AfebuBalogun).
Built with [Django](https://www.djangoproject.com/).
Used [Spotify Web API](https://developer.spotify.com/documentation/web-api) and [Rapid API Spotify Web Scraper](https://rapidapi.com/DataFanatic/api/spotify-scraper/playground/apiendpoint_65c47061-89d6-4683-bb6e-80d96c0f8aaa)

S/O to [CodeWithTomi](https://www.codewithtomi.com/)
