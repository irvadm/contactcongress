from django.conf import settings

from clients.clients import GoogleCivicRepresentativeClient, PropublicaMemberClient
from .models import Member

import logging
from pprint import pprint
import requests
import twitter


log = logging.getLogger(__name__)



class MemberUpdater(object):
    def __init__(self):
        self.propublica_client = PropublicaMemberClient()

    def update_members(self, chamber):
        log.info('Updating members of the {}...'.format(chamber))
        data = self.propublica_client.get_members(chamber) # Keys: congress, chamber, num_results, members
        chamber = data['chamber']
        members = data['members']

        # Remove members who are not in office
        for m in members:
            if m['in_office'] != True:
                log.info('Removing {} {}...'.format(m['first_name'], m['last_name']))
                members.remove(m)

        def f(member):
            return 'next_election' in member

        members = filter(f, members)

        for m in members:
            member, created = Member.objects.update_or_create(
                member_id=m['id'],
                defaults={
                    'member_id': m['id'],
                    'first_name': m['first_name'],
                    'last_name': m['last_name'],
                    'in_office': m['in_office'],
                    'party': m['party'],
                    'state': m['state'],
                    'chamber': chamber,
                    'office': m['office'],
                    'next_election': m['next_election'],
                    'phone': m['phone'],
                    'title': m['title'],
                    'website': m['url'],
                    'twitter_account': m['twitter_account'],
                    'facebook_account': m['facebook_account'],
                    'contact_page': m['contact_form'],
                }
            )
            member.clean_title()
            # Save district for house members
            if 'district' in m.keys() and member.chamber == 'House':
                member.district = m['district']

            if created:
                log.info('Created {} member: {}'.format(member.chamber, member))
            else:
                log.info('Updated {} member: {}'.format(member.chamber, member))
            member.save()



    def update_member_images(self):
        api = twitter.Api(
            consumer_key=settings.TWITTER_CONSUMER_KEY,
            consumer_secret=settings.TWITTER_SECRET_KEY,
            access_token_key=settings.TWITTER_ACCESS_TOKEN,
            access_token_secret=settings.TWITTER_ACCESS_SECRET_KEY
        )
        members = Member.objects.all()
        for m in members:
            if m.twitter_account:
                try:
                    user = api.GetUser(screen_name=m.twitter_account)
                except:
                    log.error(f'Could not find Twitter user: {m.twitter_account}')
                if user:
                    log.info('Found user: {}'.format(user))
                    if user.profile_image_url:
                        log.info('Found user image: {}'.format(user.profile_image_url))
                        try:
                            unedited_url = user.profile_image_url
                            split_url = unedited_url.split('.')
                            split_url[2] = split_url[2].replace('_normal', '')
                            joiner = '.'
                            m.image = joiner.join(split_url)
                            m.save()
                        except:
                            m.image = user.profile_image_url
                            m.save()
                else:
                    continue

def member_tasks():
    """ Job function added to task scheduler. """
    updater = MemberUpdater()
    updater.update_members(chamber='house')
    updater.update_members(chamber='senate')
    # updater.update_member_images()
