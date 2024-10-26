import os
import re
import requests
import word_counter
from selectolax.parser import HTMLParser

from word_cloud import create_word_cloud_for_artist


# Read the API token from api_token.txt
def read_api_token():
    with open('api_token.txt', 'r') as file:
        return file.read().strip()


# Your Genius API token
API_TOKEN = read_api_token()
BASE_URL = 'https://api.genius.com'

# Set up headers
headers = {'Authorization': f'Bearer {API_TOKEN}'}


def __sanitize_text(text):
    # Remove any characters that are invalid in filenames
    return re.sub(r'[<>:"/\\|?*]', '', text)


def __sanitize_lyrics(lyrics):
    # Remove any characters that are invalid in filenames
    lyrics = re.sub(r'[\[\]<>:"/\\|?*,1234567890]', ' ', lyrics)
    # Remove the words "Intro", "Verse", "Chorus", ".txt", and "---" (case-insensitive)
    lyrics = re.sub(r'\b(?:Intro|Verse|Chorus|.txt|---)\b', '', lyrics, flags=re.IGNORECASE)
    # Replace newlines and multiple spaces with a single space
    lyrics = re.sub(r'\s+', ' ', lyrics).strip()
    # Add a space before each uppercase letter that follows a lowercase letter
    lyrics = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', lyrics)
    return lyrics.upper()


def __sanitize_response(response):
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return [], []

    data = response.json()

    if len(data['response']['hits']) == 0:
        print("Error: Artist does not exist within the database.")
        return []

    if 'response' not in data or 'hits' not in data['response']:
        print("Error: Unexpected API response structure.")
        return [], []


def search_artist_songs(artist_name, max_songs=10):
    search_url = f'{BASE_URL}/search?q={artist_name}'
    response = requests.get(search_url, headers=headers)

    __sanitize_response(response)

    data = response.json()

    song_titles = []
    song_urls = []

    for hit in data['response']['hits']:
        song = hit['result']
        song_titles.append(song['title'])
        song_urls.append(song['url'])
        if len(song_titles) >= max_songs:
            break

    return song_titles, song_urls


def get_lyrics(song_url):
    page = requests.get(song_url)
    html = HTMLParser(page.text)

    # Find the lyrics of the page
    lyrics_container = html.css_first('div[data-lyrics-container="true"]')

    if lyrics_container:
        return __sanitize_lyrics(lyrics_container.text(strip=True))
    else:
        return "Lyrics not found."


def save_lyrics_to_file(title, lyrics, artist_name):
    if not os.path.exists(f'./{artist_name}'):
        os.makedirs(f'./{artist_name}')

    file_path = os.path.join(f'./{artist_name}', f'{title}.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(lyrics)


def save_word_count_to_file(word_count, artist_name):
    # Sort the word count dictionary from most common to least
    sorted_word_count = dict(sorted(word_count.items(), key=lambda item: item[1], reverse=True))

    file_path = os.path.join(f'./{artist_name}', 'word count.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"Word Count for {artist_name}:\n")
        for word, count in sorted_word_count.items():
            file.write(f"{word}: {count}\n")


def get_artist_lyrics(artist_name, max_songs=10):
    song_titles, song_urls = search_artist_songs(artist_name, max_songs)

    # If there are no songs, the artist does not exist
    if not song_titles or not song_urls:
        return

    # Create a path for the artist's name
    artist_directory = os.path.join('./', artist_name)
    if not os.path.exists(artist_directory):
        os.makedirs(artist_directory)
        print(f"Created directory: {artist_directory}")

    for title, url in zip(song_titles, song_urls):
        print(f"Downloading lyrics for {title}...")
        lyrics = get_lyrics(url)
        sanitized_title = __sanitize_text(title)
        save_lyrics_to_file(sanitized_title, lyrics, artist_name)
        print(f"Lyrics saved for {title}")

    word_count_for_artist = word_counter.word_count(artist_directory)

    # Save word count to file
    save_word_count_to_file(word_count_for_artist, artist_name)


def main():
    # artists = ["Sabrina Carpenter", "Justin Bieber", "Future", "Gucci Mane", "Jay-Z",
    #            "Ariana Grande", "Bladee", "Chief Keef", "6ix9ine", "Cocteau Twins",
    #            "Drake", "Dua Lipa", "Eminem", "Kanye West", "Kendrick Lamar", "Lauv",
    #            "Lil Yachty", "Mos Def", "Nas", "Sematary", "Skrillex", "Taylor Swift",
    #            "The Cool Kids", "The Notorious B.I.G.", "The Weeknd", "Tupac", "Wu-Tang Clan"]

    artists = ["ye"]

    # artists = ["Michael Jackson"]

    for artist in artists:
        get_artist_lyrics(artist, max_songs=100)
        create_word_cloud_for_artist(artist)


if __name__ == "__main__":
    main()
