import requests
from django.conf import settings
from pprint import pprint
import json
import urllib

class GoogleCivicClient(object):
    def __init__(self):
        self.base_url = 'https://www.googleapis.com/civicinfo/v2/'


    def get_representatives(self, **kwargs):
        """
        GET https://www.googleapis.com/civicinfo/v2/representatives?key=<YOUR_API_KEY>&address=1263%20Pacific%20Ave.%20Kansas%20City%20KS&electionId=2000
        role: legislatorLowerBody|legislatorUpperBody|
        parameters: address, roles, 
        """
        parameters = {
            'key': settings.GOOGLE_CIVIC_API_KEY
        }

        if kwargs['roles']:
            parameters['roles'] = kwargs.get('roles')

        if kwargs['address']:
            parameters['address'] = kwargs.get('address')
        qualifier = 'representatives'

        path = self.base_url + qualifier
        print(f'PATH: {path}')
        res = requests.get(path, params=parameters) 
        print(f'RESPONSE URL: {res.url}')
        if res.status_code == 200:
            data = res.json()
            print(data.keys())
            print(data['kind'])
            print('*' * 50)
            print(data['normalizedInput'])

            return data['officials']
        else:
            self.handle_error(res.status_code)



    def handle_error(self, status_code):
        status_code = int(status_code)
        if status_code == 400:
            # print('[!] [{}] Bad Request'.format(status_code))
            raise Exception('[!] [{}] Bad Request'.format(status_code))
        elif status_code == 401:
            # print('[!] [{}] Authentication Failed'.format(status_code))
            raise Exception('[!] [{}] Authentication Failed'.format(status_code))
        elif status_code == 404:
            # print('[!] [{}] URL not found'.format(status_code))
            raise Exception('[!] [{}] URL not found'.format(status_code))
        elif status_code >= 300:
            # print('[!] [{}] Unexpected Redirect'.format(status_code))
            raise Exception('[!] [{}] Unexpected Redirect'.format(status_code))
        elif status_code >= 500:
            # print('[!] [{}] Server Error'.format(status_code))
            raise Exception('[!] [{}] Server Error'.format(status_code))
        else:
            # print('Error unknown.')
            raise Exception('Error unknown.')
        
