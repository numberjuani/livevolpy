import os
from typing import Dict 
import json
import time
import requests

class LiveVolClient:
    _BASE_URL: str = 'https://api.livevol.com/v1/'
    _LIVE_ENDPOINT:str =   "https://api.livevol.com/v1/"
    _AUTH_FILENAME:str = 'cboe_auth.json'
    _AUTH_ENDPOINT:str = 'https://id.livevol.com/connect/token'

    def __init__(self, client_id, client_secret):
        """Initialize the LiveVolClient object"""
        self.client_id = client_id
        self.client_secret = client_secret

    def authorize(self):
        """This function attempts to retrive auth info from a local json file, if it doesn't exist, it will attempt to get it from the livevol api. 
        If the auth file exists but is expired, it will delete the expired one, and attempt to get a new one."""
        if os.path.exists(self._AUTH_FILENAME):
            print('Attempting to get auth token from file...')
            file = open(self._AUTH_FILENAME)
            auth = json.load(file)
            file.close()
            if auth['expiration_time'] >= time.time():
                self.access_token = auth['access_token']
                self.token_expiry_time = auth['expiration_time']
            else:
                os.remove(self._AUTH_FILENAME)
                (token,expiry) = self._send_auth_request()
                self.access_token = token
                self.token_expiry_time = expiry
        else:
            (token,expiry) = self._send_auth_request()
            self.access_token = token
            self.token_expiry_time = expiry

    def _send_auth_request(self):
        """This function sends the auth request to the livevol api, and returns the access token, it is private because it should only be called by get_auth"""
        print('Attempting to get auth token...')
        body = 'grant_type=client_credentials'
        request = requests.post(self._AUTH_ENDPOINT, data=body, auth=(
            self.client_id,self.client_secret))
        print(f'Auth Request HTTP Status Code {request.status_code}')
        try:
            auth_request = request.json()
            auth_request['expiration_time'] = time.time() + auth_request['expires_in']
            with open('cboe_auth.json', 'w') as f:
                json.dump(auth_request, f)
            return (auth_request['access_token'], auth_request['expiration_time'])
        except Exception:
            print('Error: Could not get auth token')
            print(f'Auth Request Headers {request.headers}')
            return (None, None)
    
    def _check_token_is_valid(self):
        """This function checks if the access token is valid, if it is not, it will attempt to get a new one"""
        if self.token_expiry_time < time.time():
            self.get_auth()
    
    def get_options_and_underlying_quotes(self,params:Dict[str, str]):
        """This function gets the options and underlying quotes from the livevol api"""
        self._check_token_is_valid()
        request = requests.get(self._BASE_URL+'live/allaccess/market/option-and-underlying-quotes', headers={'Authorization': f'Bearer {self.access_token}'},params=params)
        print(f'Options and Underlying Quotes Request HTTP Status Code for {params["symbol"]}: {request.status_code}')
        try:
            if request.status_code == 200:
                print(f'Monthly points used: {request.headers["x-monthly-points-used"]}')
                ret_value = request.json()
                return ret_value
        except Exception:
            print(f'Error: Could not get options and underlying quotes for {params["symbol"]}')
            print(f'Options and Underlying Quotes Request Headers for {params["symbol"]}: {request.headers}')
            return None
    
    def get_underlying_quotes(self,params:Dict[str, str]):
        """This function obtains underlying quotes"""
        self._check_token_is_valid()
        request = requests.get(self._BASE_URL+'live/allaccess/market/underlying-quotes', headers={'Authorization': f'Bearer {self.access_token}'},params=params)
        try:
            if request.status_code == 200:
                print(f'Monthly points used: {request.headers["x-monthly-points-used"]}')
                ret_value = request.json()
                return ret_value
        except Exception:
            print(f'Error: Could not get underlying quotes for {params["symbol"]}')
            print(f'Underlying Quotes Request Headers for {params["symbol"]}: {request.headers}')
            return None
    
    def get_trades(self,params:Dict[str, str]):
        """This function obtains trade data"""
        self._check_token_is_valid()
        request = requests.get(self._BASE_URL+'live/allaccess/market/all-option-trades', headers={'Authorization': f'Bearer {self.access_token}'},params=params)
        try:
            if request.status_code == 200:
                print(f'Monthly points used: {request.headers["x-monthly-points-used"]}')
                ret_value = request.json()
                return ret_value
        except Exception:
            print(f'Error: Could not get trades for {params["symbol"]}')
            print(f'Trades Request Headers for {params["symbol"]}: {request.headers}')
            return None
    
    def get_option_trades_breakdown(self,params:Dict[str, str]):
        """This options retrives the options trades breakdown"""
        self._check_token_is_valid()
        request = requests.get(self._BASE_URL+'live/allaccess/market/option-trades-breakdown', headers={'Authorization': f'Bearer {self.access_token}'},params=params)
        try:
            if request.status_code == 200:
                print(f'Monthly points used: {request.headers["x-monthly-points-used"]}')
                ret_value = request.json()
                return ret_value
        except Exception:   
            print(f'Error: Could not get trades for {params["symbol"]}')
            print(f'Trades Request Headers for {params["symbol"]}: {request.headers}')
            return None
    
    def get_flex_trades(self,params):
        """This function obtains flex trades"""
        self._check_token_is_valid()
        request = requests.get(self._BASE_URL+'live/allaccess/market/flex-trades', headers={'Authorization': f'Bearer {self.access_token}'},params=params)
        try:
            if request.status_code == 200:
                print(f'Monthly points used: {request.headers["x-monthly-points-used"]}')
                ret_value = request.json()
                return ret_value
        except Exception:
            print(f'Error: Could not get flex trades for {params["symbol"]}')
            print(f'Flex Trades Request Headers for {params["symbol"]}: {request.headers}')
            return None
    
    def get_halts(self,params):
        """This function obtains halts"""
        self._check_token_is_valid()
        request = requests.get(self._BASE_URL+'live/allaccess/market/halts', headers={'Authorization': f'Bearer {self.access_token}'},params=params)
        try:
            if request.status_code == 200:
                print(f'Monthly points used: {request.headers["x-monthly-points-used"]}')
                ret_value = request.json()
                return ret_value
        except Exception:
            print(f'Error: Could not get halts for {params["symbol"]}')
            print(f'Halts Request Headers for {params["symbol"]}: {request.headers}')
            return None
    
    def get_underlying_limit_updn(self,params):
        """This function obtains underlying limit up/down"""
        self._check_token_is_valid()
        request = requests.get(self._BASE_URL+'live/allaccess/market/underlying-limit-up-limit-down', headers={'Authorization': f'Bearer {self.access_token}'},params=params)
        try:
            if request.status_code == 200:
                print(f'Monthly points used: {request.headers["x-monthly-points-used"]}')
                ret_value = request.json()
                return ret_value
        except Exception:
            print(f'Error: Could not get underlying limit up/down for {params["symbol"]}')
            print(f'Underlying Limit Up/Down Request Headers for {params["symbol"]}: {request.headers}')
            return None


def create_json_file(filepath:str,data:Dict):
    """This function creates a json file"""
    with open(filepath, 'w') as f:
        json.dump(data, f)