import pandas as pd
import requests
import base64

# Spotify Credentials
client_id = "776d44e399104c049eaf2c9cce2d31c1"
client_secret = "a018aa94930d4c0bb5fcb60b5ecd0887"

# Step 1: Function to Get Access Token
def get_spotify_token(client_id, client_secret):
    auth_url = "https://accounts.spotify.com/api/token"
    auth_data = {'grant_type': 'client_credentials'}
    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {client_creds_b64}",
    }
    
    response = requests.post(auth_url, data=auth_data, headers=headers)
    token_data = response.json()
    
    return token_data['access_token']

# Step 2: Function to Search Spotify and Fetch Album/Track Image URLs
def search_spotify_track(track_name, artist_name, token):
    search_url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    query = f"track:{track_name} artist:{artist_name}"
    params = {
        "q": query,
        "type": "track",
        "limit": 1
    }
    
    response = requests.get(search_url, headers=headers, params=params)
    results = response.json()
    
    try:
        track_info = results['tracks']['items'][0]
        return track_info['album']['images'][0]['url']  # URL of album cover image
    except (IndexError, KeyError):
        return None  # In case no results are found

# Step 3: Load the Spotify Dataset and Add Album Cover URLs
def add_album_cover_urls_to_dataset(file_path, client_id, client_secret):
    # Load the dataset
    df = pd.read_csv(file_path, encoding='ISO-8859-1')

    # Get access token
    token = get_spotify_token(client_id, client_secret)

    # Create a new column for album cover URLs
    df['album_cover_url'] = df.apply(lambda row: search_spotify_track(row['track_name'], row['artist(s)_name'], token), axis=1)

    # Save the updated dataset
    df.to_excel("spotify_2023_with_cover_urls.xlsx", index=False)

    return df

# Step 4: Run the Script to Update Dataset
file_path = "spotify-2023.csv"  # Replace with your actual file path
updated_df = add_album_cover_urls_to_dataset(file_path, client_id, client_secret)
pd.set_option('display.max_colwidth', None)
print(updated_df.head(10))
