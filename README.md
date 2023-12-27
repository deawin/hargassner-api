
# Hargassner API

This Python module enables you to query information about your Hargassner devices from their Web portal.

Your device must be connected to the Web portal of Hargassner (https://web.hargassner.at). To use the module, you will
need access to the following information:

| Information     | Description                                                                                                                                                                                                                                                                                                                                    |
|-----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Username        | This is your username that you use to log into the web portal.                                                                                                                                                                                                                                                                                 |
| Password        | This is your password that you use to log into the web portal.                                                                                                                                                                                                                                                                                 |
| Client Secret   | The client secret is a cryptographic key derived from your login information. It can be found in the developer tools from your browser while navigating the web portal. Look for a POST request "login" and inspect the JSON information that is sent to the Hargassner server. It will contain your username, password and the client secret. |
| Installation ID | This is the ID of your installation. You can find it in the address bar of your browser when you navigate through the web portal (https://web.hargassner.at/installations/<name>-<installation-id>/info).                                                                                                                                      |


## Usage/Examples

```python
from hargassner.client import HargassnerAPI

# MAIN
if __name__ == "__main__":
    h = HargassnerAPI()
    h.username = '<your Hargassner username>'
    h.password = '<your Hargassner password>'
    h.client_secret = '<your client secret from Hargassner web'
    h.installation = '<your Hargassner installation ID>'
    h.authdat = 'auth.dat'
    h.debug = True
    j = h.query_api()

    if 'data' in j:
        for w in j['data']:
            if w['widget'] == 'EVENTS':
                for e in w['values']:
                    print('Ereignis: ' +e['created_at'] + " -> "+ e['text'])
            elif w['widget'] == 'HEATER':
                print('Name:' + w['values']['name'])
                print('State:' + w['values']['state'])
                print('Abgastemperatur: ' + str(w['values']['smoke_temperature']))
                print('Kesseltemperatur: ' + str(w['values']['heater_temperature_current']))
                print('Aussentemperatur: ' + str(w['values']['outdoor_temperature']))
            elif w['widget'] == 'BUFFER':
                print('Puffer Füllgrad: ' + str(w['values']['buffer_charge']))
                print('Puffer Temperatur Oben: ' + str(w['values']['buffer_temperature_top']))
                print('Puffer Temperatur Mitte: ' + str(w['values']['buffer_temperature_center']))
                print('Puffer Temperatur Unten: ' + str(w['values']['buffer_temperature_bottom']))
    else:
        print("PROBLEM")

```

