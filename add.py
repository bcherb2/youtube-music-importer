from ytmusicapi import YTMusic
import csv
import os
import time

MAX_RETRIES = 4 # times
DELAY = 10  # seconds
TRACK_COL = 'Track Name'  # Modify this to the header name for tracks in your CSV
ARTIST_COL = 'Artist Name(s)'  # Modify this to the header name for artists in your CSV



yt = YTMusic('oauth.json')

# Fetch existing playlists once
existing_playlists = {playlist['title']: playlist['playlistId'] for playlist in yt.get_library_playlists()}

delay = DELAY

def get_or_create_playlist(name):
    if name in existing_playlists:
        return existing_playlists[name]
    
    playlist_id = yt.create_playlist(name, name + ' description')
    existing_playlists[name] = playlist_id
    return playlist_id

csv_files = [file for file in os.listdir() if file.endswith('.csv')]

try:
    for csv_file in csv_files:
        playlist_name = os.path.splitext(csv_file)[0] 
        playlistId = get_or_create_playlist(playlist_name)
        
        with open(csv_file, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                time.sleep(1)
                track = row[TRACK_COL]
                artist = row[ARTIST_COL]
                search_query = f"{track} {artist}"
                search_results = yt.search(search_query)
                

                retries = 0
                success = False

                while retries < MAX_RETRIES and not success:
                    try:
                        if search_results:
                            song_id = None
                            for result in search_results:
                                if 'videoId' in result:
                                    song_id = result['videoId']
                                    break

                            if song_id:
                                yt.add_playlist_items(playlistId, [song_id])
                                print(f"Successfully added '{track}' by {artist} to playlist '{playlist_name}'.")
                                success = True
                            else:
                                print(f"No valid videoId found for '{track}' by {artist}.")
                                success = True  # No point in retrying if song wasn't found
                        else:
                            print(f"Couldn't find '{track}' by {artist} in the search results.")
                            success = True  # No point in retrying if song wasn't found

                    except Exception as e:
                        if "HTTP 400" in str(e) or "HTTP 429" in str(e):  # 429 is typical for rate limit errors
                            print(f"Rate limit error for '{track}' by {artist}. Retrying in {delay} seconds...")
                            time.sleep(delay)
                            delay *= 2  # Double the delay for exponential backoff
                            retries += 1
                        else:
                            print(f"An error occurred while adding '{track}' by {artist} to playlist '{playlist_name}': {e}")
                            retries = MAX_RETRIES  # Don't retry for other errors

                # Reset delay for next song
                delay = DELAY

except Exception as e:
    print(f"An error occurred: {e}")

print("Finished processing all CSV files!")
