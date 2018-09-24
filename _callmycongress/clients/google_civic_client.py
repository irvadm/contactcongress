import requests
from django.conf import settings
from pprint import pprint
import json
from write_to_file import python_to_json

class GoogleCivicClient(object):
    def __init__(self):
        self.base_url = 'https://www.googleapis.com/civicinfo/v2/'

    def get_representatives(self, address):
        url =  self.base_url + 'representatives' + '?' + 'key=' + settings.GOOGLE_CIVIC_API_KEY + '&address=' + '{}'.format(address)
        print(url)
        res = requests.get(url)
        data = res.json()
        with open('google_civic_get_representatives.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
        return data['officials']
        #data.keys() = dict_keys(['kind', 'normalizedInput', 'divisions', 'offices', 'officials'])
        #type(data['officials']) = list
        # officials = data['officials']

        # return data

