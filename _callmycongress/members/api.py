from .models import Member
from clients.clients import GoogleCivicRepresentativeClient, PropublicaMemberClient

import logging

log = logging.getLogger(__name__)


class MemberUpdater(object):
    def __init__(self):
        self.client = PropublicaMemberClient()

    def update_members(self, chamber):
        log.info('Updating members of the {}...'.format(chamber))
        data = self.client.get_members(chamber) # Keys: congress, chamber, num_results, members
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
                }
            )
            # Save district for house members
            if 'district' in m.keys() and member.chamber == 'House':
                member.district = m['district']

            if created:
                log.info('Created {} member: {}'.format(member.chamber, member))
            else:
                log.info('Updated {} member: {}'.format(member.chamber, member))
            member.save()

def member_tasks():
    """ Job function added to task scheduler. """
    crawler = MemberUpdater()
    crawler.update_members(chamber='house')
    crawler.update_members(chamber='senate')