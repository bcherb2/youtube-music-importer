
# YouTube Music Playlist Importer

A Python utility to automatically create and update playlists on YouTube Music using CSV files.

## Description

This tool was made for taking exported CSVs from Spotify and being able to ingest them into Youtube Music.  But, it should work for just about any CSV formatted music list.  It does depend on the [ytmusicapi](https://ytmusicapi.readthedocs.io/en/stable/) library, which is a third party library.  I have no affiliation with the author of that library.

## Prerequisites

- Python 3.x
- A `oauth.json` file containing credentials for the YouTube Music API. To generate this file, follow the authentication steps provided in the [ytmusicapi documentation](https://ytmusicapi.readthedocs.io/en/stable/usage.html).

## Installation

1. Clone the repository:
```bash
git clone https://github.com/bcherb2/youtube-music-importer.git yt-music-importer
```

2. Change directory into the cloned repository:
```bash
cd yt-music-importer
```

3. Install the required Python packages:
```bash
pip install ytmusicapi
```

## Usage

1. Prepare your CSV files. Each CSV file should represent one playlist. The script will use the exact filename of the CSV to become (or update) the playlist.  I used [Exportify](https://exportify.net/) to export my Spotify playlists to CSV.
   
   To ensure compatibility, make sure you modify the column header variables `TRACK_COL` and `ARTIST_COL` in the script to match the column headers of your CSV files.

2. Place the CSV files in the same directory as the script.

3. Run the script:
```bash
python add.py
```

4. The script will iterate over each CSV file, creating or updating the corresponding playlist on YouTube Music with the  tracks specified in the CSV.

If everything worked as intended, you should see something like this:

```bash
    >python .\add.py
    Successfully added 'Put Your Hands Up For Detroit - Radio Edit' by Fedde Le Grand to playlist 'test'.
    Successfully added 'Innocence' by NERO to playlist 'test'.
    Successfully added 'Pressure - Alesso Remix' by Nadia Ali,Starkillers,Alex Kenji,Alesso to playlist 'test'.
```

## Error Handling

The script implements error handling mechanisms like retrying on rate limit errors and exponential backoff; you may need to adjust if you run into issues.
