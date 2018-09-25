from django.conf import settings

from pprint import pprint
import requests
import logging

log = logging.getLogger(__name__)


class PropublicaClient(object):
    def __init__(self):
        self.BASE_URL = "https://api.propublica.org/congress/v1/"
        self.API_KEY = settings.PROPUBLICA_CONGRESS_API_KEY

    def parse(self, content):
        return content['results'][0]

    def fetch(self, path):
        """
        Make an API request, with authentication.
        """
        url = self.BASE_URL + path
        log.debug('URL: {}'.format(url))
        headers = {'X-API-Key': self.API_KEY}

        resp = requests.get(url, headers=headers)
        content = resp.json() # Convert str to python dict keys=['status': 'OK', 'copyright': 'Copyright 2018...', 'results': []]

        # Handle requests error response
        if resp.status_code != 200:
            self.handle_error(resp.status_code)

        log.info('API RESPONSE STATUS: {}'.format(content['status']))
        # Handle API error response
        if content['status'] != 'OK':
            if 'error' in content.keys():
                log.error('ERROR: {}'.format(content['error']))
            self.handle_error(content['status'])

        return self.parse(content)
    
class PropublicaMemberClient(PropublicaClient):
    def get_members(self, chamber, congress='115'):
        """
        Gets all members of a specific chamber.
        GET https://api.propublica.org/congress/v1/{congress}/{chamber}/members.json
        Returns: {
            'congress': '115',
            'chamber': 'House',
            'num_results': 435,
            'members': [ { id: A000360, first_name: Lamar, last_name: Alexander }, { ... }, { ... } ]
        }
        """
        path = '{}/{}/members.json'.format(congress, chamber)
        content = self.fetch(path)
        return content

    def get_member(self, member_id):
        """
        Gets a specific member of congress.
        GET https://api.propublica.org/congress/v1/members/{member-id}.json
        Returns: {
            "member_id": "K000388",

            "first_name": "Trent",
            "last_name": "Kelly",
            "url": "https://trentkelly.house.gov",
            "twitter_account": "reptrentkelly",
            "in_office": true,
            "current_party": "R",
            "last_updated": "2018-06-14 17:01:27 -0400",
            "roles": [{
                "congress": "115",
                "chamber": "House",
                "title": "Representative",
                "short_title": "Rep.",
                "state": "MS",
                "party": "R",
                "leadership_role": null,
                "fec_candidate_id": "H6MS01131",
                "seniority": "4",
                "district": "1",
                "at_large": false,
                "ocd_id": "ocd-division/country:us/state:ms/cd:1",
                "start_date": "2017-01-03",
                "end_date": "2019-01-03",
                "office": "1721 Longworth House Office Building",
                "phone": "202-225-4306",
                "fax": null,
                "contact_form": null,
                "bills_sponsored": 7,
                "bills_cosponsored": 146,
                "missed_votes_pct": 0.51,
                "votes_with_party_pct": 96.92,
                "committees": [{
                        "name": "Committee on Agriculture",
                        "code": "HSAG",
                        "api_uri": "https://api.propublica.org/congress/v1/115/house/committees/HSAG.json",
                        "side": "majority",
                        "title": "Member",
                        "rank_in_party": 20,
                        "begin_date": "",
                        "end_date": "2019-01-03"
                    },
                    {
                        "name": "Committee on Armed Services",
                        "code": "HSAS",
                        "api_uri": "https://api.propublica.org/congress/v1/115/house/committees/HSAS.json",
                        "side": "majority",
                        "title": "Member",
                        "rank_in_party": 28,
                        "begin_date": "",
                        "end_date": "2019-01-03"
                    },
        """
        path = "members/{}.json".format(member_id)
        content = self.fetch(path)
        log.info('Member ID: {}, Name: {} {}'.format(content['member_id'], content['first_name'], content['last_name']))
        return content


class GoogleCivicClient(object):
    def __init__(self):
        self.BASE_URL = 'https://www.googleapis.com/civicinfo/v2/'
        self.API_KEY = settings.GOOGLE_CIVIC_API_KEY

class GoogleCivicRepresentativeClient(GoogleCivicClient):

    def get_representatives(self, qualifier='representatives', **kwargs):
        """
        GET https://www.googleapis.com/civicinfo/v2/representatives?key=<YOUR_API_KEY>&address=1263%20Pacific%20Ave.%20Kansas%20City%20KS&electionId=2000
        role: legislatorLowerBody|legislatorUpperBody|
        parameters: address, roles, 
        """
        parameters = {
            'key': self.API_KEY
        }

        if kwargs['roles']:
            parameters['roles'] = kwargs.get('roles')

        if kwargs['address']:
            parameters['address'] = kwargs.get('address')

        # Make path
        path = self.BASE_URL + qualifier
        log.info(f'PATH: {path}')

        # Make call to Google Civic API
        res = requests.get(path, params=parameters) 
        log.info(f'RESPONSE URL: {res.url}')

        # Check if response is successful
        if res.status_code == 200:
            data = res.json()
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
        
