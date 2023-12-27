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
                    return data['xsrf_token'], data['bearer']
            except IOError as e:
                if self.debug: print("auth.dat not present. Forcing login.")
                pass

        # GET XSRF-TOKEN FROM LOGIN PAGE
        response = requests.get('https://web.hargassner.at/login')
        xsrf_token = response.headers['set-cookie']
        xsrf_header = {
            'X-XSRF-TOKEN': xsrf_token,
        }
        xsrf_token = xsrf_token.split(';')[0]

        if self.debug: print('xsrf-token: ' + xsrf_token)

        # LOGIN
        login_data = {
            'email': self.username,
            'password': self.password,
            'client_id': '1',
            'client_secret': self.client_secret,
        }

        response = requests.post('https://web.hargassner.at/api/auth/login', headers=xsrf_header, data=login_data,
                                 verify=True)
        j = response.json()
        bearer = j['access_token']

        if self.debug: print('login response: ')
        if self.debug: print(j)
        if self.debug: print('bearer: ' + bearer)

        with open(self.authdat, 'wb') as file:
            data = {'xsrf_token': xsrf_token, 'bearer': bearer}
            pickle.dump(data, file)
            file.close()

        return xsrf_token, bearer

    def query_api(self):
        xsrf_token, bearer = self.login()

        # DEVICE QUERY API
        authentication_header = {
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + bearer,
            'X-XSRF-TOKEN': xsrf_token,
        }

        response = requests.get('https://web.hargassner.at/api/installations/' + self.installation + '/widgets',
                                headers=authentication_header, verify=True)
        j = response.json()
        if self.debug: print('widgets response: ')
        if self.debug: print(j)

        if 'message' in j and j['message'] == 'Unauthenticated.':
            # We're unauthenticated. Force login and try again.
            xsrf_token, bearer = self.login(True)

            authentication_header = {
                'Accept': 'application/json',
                'Authorization': 'Bearer ' + bearer,
                'X-XSRF-TOKEN': xsrf_token,
            }

            response = requests.get('https://web.hargassner.at/api/installations/' + self.installation + '/widgets',
                                    headers=authentication_header, verify=True)
            j = response.json()
            if self.debug: print('widgets response: ')
            if self.debug: print(j)

        return j
