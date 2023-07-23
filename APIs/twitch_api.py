import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from decouple import config

class StreamerNotFoundError(Exception):
    pass

class TwitchAPI:
    def __init__(self):
        self.client_id = config('TWITCH_CLIENT_ID')
        self.client_secret = config('TWITCH_CLIENT_SECRET')
        self.headers = {
            'Client-ID': self.client_id,
            'Authorization': 'Bearer ' + self._get_access_token(),
        }
        self.session = self._create_session()

    def _get_access_token(self):
        body = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials',
        }
        response = requests.post('https://id.twitch.tv/oauth2/token', body)
        response.raise_for_status()
        keys = response.json()
        return keys['access_token']

    def _create_session(self):
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('https://', adapter)
        return session

    def check_stream_status(self, streamer_name):
        url = f'https://api.twitch.tv/helix/streams?user_login={streamer_name}'
        response = self.session.get(url, headers=self.headers)
        response.raise_for_status()
        stream_data = response.json()

        if len(stream_data['data']) == 1:
            return (
                True,
                stream_data["data"][0]['viewer_count'],
                stream_data["data"][0]['game_name'],
                f"https://static-cdn.jtvnw.net/ttv-boxart/{stream_data['data'][0]['game_id']}-285x380.jpg",
            )
        else:
            return False

    def check_streamer_existence(self, streamer_name):
        url = f'https://api.twitch.tv/helix/users?login={streamer_name}'
        response = self.session.get(url, headers=self.headers)
        response.raise_for_status()
        stream_data = response.json()
        return bool(stream_data['data'])

    def get_user_info_by_name(self, streamer_name):
        url = f'https://api.twitch.tv/helix/users?login={streamer_name}'
        response = self.session.get(url, headers=self.headers)
        response.raise_for_status()
        stream_data = response.json()
        return stream_data["data"]

