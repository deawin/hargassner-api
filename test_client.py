#!/usr/bin/python
import unittest
from unittest.mock import patch, MagicMock
from hargassner.client import HargassnerAPI

class TestHargassnerAPI(unittest.TestCase):
    def setUp(self):
        self.api = HargassnerAPI()
        self.api.username = 'test_user'
        self.api.password = 'test_password'
        self.api.client_secret = 'test_secret'
        self.api.installation = 'test_installation'
        self.api.authdat = 'test_auth.dat'
        self.api.debug = False

    @patch('hargassner.client.requests.get')
    @patch('hargassner.client.requests.post')
    @patch('hargassner.client.pickle.load')
    @patch('hargassner.client.open')
    def test_missing_data_key(self, mock_open, mock_pickle_load, mock_post, mock_get):
        # Mock login
        mock_response = MagicMock()
        mock_response.headers = {'set-cookie': 'XSRF-TOKEN=test_token;'}
        mock_get.return_value = mock_response

        mock_post_response = MagicMock()
        mock_post_response.json.return_value = {'access_token': 'test_bearer'}
        mock_post.return_value = mock_post_response

        # Mock API response with missing 'data' key
        mock_api_response = MagicMock()
        mock_api_response.json.return_value = {'message': 'Success'}
        mock_get.return_value = mock_api_response

        # Call the method
        result = self.api.query_api()

        # Check that 'data' key was added with an empty list
        self.assertIn('data', result)
        self.assertEqual(result['data'], [])

    @patch('hargassner.client.requests.get')
    @patch('hargassner.client.requests.post')
    @patch('hargassner.client.pickle.load')
    @patch('hargassner.client.open')
    def test_missing_widget_key(self, mock_open, mock_pickle_load, mock_post, mock_get):
        # Mock login
        mock_response = MagicMock()
        mock_response.headers = {'set-cookie': 'XSRF-TOKEN=test_token;'}
        mock_get.return_value = mock_response

        mock_post_response = MagicMock()
        mock_post_response.json.return_value = {'access_token': 'test_bearer'}
        mock_post.return_value = mock_post_response

        # Mock API response with widget missing 'widget' key
        mock_api_response = MagicMock()
        mock_api_response.json.return_value = {'data': [{'values': {}}]}
        mock_get.return_value = mock_api_response

        # Call the method
        result = self.api.query_api()

        # Check that 'widget' key was added with default value
        self.assertEqual(result['data'][0]['widget'], 'UNKNOWN')

    @patch('hargassner.client.requests.get')
    @patch('hargassner.client.requests.post')
    @patch('hargassner.client.pickle.load')
    @patch('hargassner.client.open')
    def test_missing_values_key(self, mock_open, mock_pickle_load, mock_post, mock_get):
        # Mock login
        mock_response = MagicMock()
        mock_response.headers = {'set-cookie': 'XSRF-TOKEN=test_token;'}
        mock_get.return_value = mock_response

        mock_post_response = MagicMock()
        mock_post_response.json.return_value = {'access_token': 'test_bearer'}
        mock_post.return_value = mock_post_response

        # Mock API response with widgets missing 'values' key
        mock_api_response = MagicMock()
        mock_api_response.json.return_value = {
            'data': [
                {'widget': 'HEATER'},
                {'widget': 'EVENTS'},
                {'widget': 'BUFFER'}
            ]
        }
        mock_get.return_value = mock_api_response

        # Call the method
        result = self.api.query_api()

        # Check that 'values' key was added with appropriate default value
        # For HEATER, check that default values were added
        heater_values = result['data'][0]['values']
        self.assertEqual(heater_values['name'], 'Unknown')
        self.assertEqual(heater_values['state'], 'Unknown')
        self.assertEqual(heater_values['smoke_temperature'], 0)
        self.assertEqual(heater_values['heater_temperature_current'], 0)
        self.assertEqual(heater_values['outdoor_temperature'], 0)

        self.assertEqual(result['data'][1]['values'], [])  # EVENTS should get empty list

        # For BUFFER, check that default values were added
        buffer_values = result['data'][2]['values']
        self.assertEqual(buffer_values['buffer_charge'], 0)
        self.assertEqual(buffer_values['buffer_temperature_top'], 0)
        self.assertEqual(buffer_values['buffer_temperature_center'], 0)
        self.assertEqual(buffer_values['buffer_temperature_bottom'], 0)

    @patch('hargassner.client.requests.get')
    @patch('hargassner.client.requests.post')
    @patch('hargassner.client.pickle.load')
    @patch('hargassner.client.open')
    def test_missing_heater_values(self, mock_open, mock_pickle_load, mock_post, mock_get):
        # Mock login
        mock_response = MagicMock()
        mock_response.headers = {'set-cookie': 'XSRF-TOKEN=test_token;'}
        mock_get.return_value = mock_response

        mock_post_response = MagicMock()
        mock_post_response.json.return_value = {'access_token': 'test_bearer'}
        mock_post.return_value = mock_post_response

        # Mock API response with HEATER widget missing some values
        mock_api_response = MagicMock()
        mock_api_response.json.return_value = {
            'data': [
                {
                    'widget': 'HEATER',
                    'values': {
                        'name': 'Test Heater',
                        # Missing other values
                    }
                }
            ]
        }
        mock_get.return_value = mock_api_response

        # Call the method
        result = self.api.query_api()

        # Check that missing values were added with default values
        heater_values = result['data'][0]['values']
        self.assertEqual(heater_values['name'], 'Test Heater')  # Original value preserved
        self.assertEqual(heater_values['state'], 'Unknown')
        self.assertEqual(heater_values['smoke_temperature'], 0)
        self.assertEqual(heater_values['heater_temperature_current'], 0)
        self.assertEqual(heater_values['outdoor_temperature'], 0)

    @patch('hargassner.client.requests.get')
    @patch('hargassner.client.requests.post')
    @patch('hargassner.client.pickle.load')
    @patch('hargassner.client.open')
    def test_missing_buffer_values(self, mock_open, mock_pickle_load, mock_post, mock_get):
        # Mock login
        mock_response = MagicMock()
        mock_response.headers = {'set-cookie': 'XSRF-TOKEN=test_token;'}
        mock_get.return_value = mock_response

        mock_post_response = MagicMock()
        mock_post_response.json.return_value = {'access_token': 'test_bearer'}
        mock_post.return_value = mock_post_response

        # Mock API response with BUFFER widget missing some values
        mock_api_response = MagicMock()
        mock_api_response.json.return_value = {
            'data': [
                {
                    'widget': 'BUFFER',
                    'values': {
                        'buffer_charge': 75,
                        # Missing other values
                    }
                }
            ]
        }
        mock_get.return_value = mock_api_response

        # Call the method
        result = self.api.query_api()

        # Check that missing values were added with default values
        buffer_values = result['data'][0]['values']
        self.assertEqual(buffer_values['buffer_charge'], 75)  # Original value preserved
        self.assertEqual(buffer_values['buffer_temperature_top'], 0)
        self.assertEqual(buffer_values['buffer_temperature_center'], 0)
        self.assertEqual(buffer_values['buffer_temperature_bottom'], 0)

if __name__ == '__main__':
    unittest.main()
