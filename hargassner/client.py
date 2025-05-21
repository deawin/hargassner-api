#!/usr/bin/python
import requests
import pickle


class HargassnerAPI:
    """

    """
    username = ''
    password = ''
    client_secret = ''
    installation = ''
    authdat = ''
    debug = False

    def __init__(self):
        pass

    def login(self, force=False):
        if not force:
            try:
                with open(self.authdat, 'rb') as file:
                    data = pickle.load(file)
                    file.close()
                    return data['bearer']
            except IOError as e:
                if self.debug: print("auth.dat not present. Forcing login.")
                pass

        # LOGIN
        login_data = {
            'email': self.username,
            'password': self.password,
            'client_id': '1',
            'client_secret': self.client_secret,
        }

        response = requests.post('https://web.hargassner.at/api/auth/login', data=login_data, verify=True)
        j = response.json()
        bearer = j['access_token']

        if self.debug: print('login response: ')
        if self.debug: print(j)
        if self.debug: print('bearer: ' + bearer)

        with open(self.authdat, 'wb') as file:
            data = {'bearer': bearer}
            pickle.dump(data, file)
            file.close()

        return bearer

    def query_api(self):
        bearer = self.login()

        # DEVICE QUERY API
        authentication_header = {
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + bearer,
        }

        response = requests.get('https://web.hargassner.at/api/installations/' + self.installation + '/widgets',
                                headers=authentication_header, verify=True)
        j = response.json()
        if self.debug: print('widgets response: ')
        if self.debug: print(j)

        if 'message' in j and j['message'] == 'Unauthenticated.':
            # We're unauthenticated. Force login and try again.
            bearer = self.login(True)

            authentication_header = {
                'Accept': 'application/json',
                'Authorization': 'Bearer ' + bearer,
            }

            response = requests.get('https://web.hargassner.at/api/installations/' + self.installation + '/widgets',
                                    headers=authentication_header, verify=True)
            j = response.json()
            if self.debug: print('widgets response: ')
            if self.debug: print(j)

        # Check for presence of expected parameters and set defaults if not present
        if 'data' not in j:
            j['data'] = []

        for widget in j['data']:
            if 'widget' not in widget:
                widget['widget'] = 'UNKNOWN'

            if 'values' not in widget:
                if widget['widget'] == 'EVENTS':
                    widget['values'] = []
                else:
                    widget['values'] = {}

            # Set default values for specific widget types
            if widget['widget'] == 'HEATER' and isinstance(widget['values'], dict):
                default_heater_values = {
                    'name': 'Unknown',
                    'state': 'Unknown',
                    'smoke_temperature': 0,
                    'heater_temperature_current': 0,
                    'outdoor_temperature': 0
                }
                for key, default_value in default_heater_values.items():
                    if key not in widget['values']:
                        widget['values'][key] = default_value

            elif widget['widget'] == 'BUFFER' and isinstance(widget['values'], dict):
                default_buffer_values = {
                    'buffer_charge': 0,
                    'buffer_temperature_top': 0,
                    'buffer_temperature_center': 0,
                    'buffer_temperature_bottom': 0
                }
                for key, default_value in default_buffer_values.items():
                    if key not in widget['values']:
                        widget['values'][key] = default_value

        return j
