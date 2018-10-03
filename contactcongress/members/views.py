from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, reverse

from clients.clients import GoogleCivicRepresentativeClient
from .models import Member
from .utils import remove_middle_initial

import logging
from pprint import pprint

logger = logging.getLogger(__name__)


def members(request):
    if not request.GET.get('address'):
        return render(request, '400.html')
    address = request.GET.get('address', '')
    logger.info(f'ADDRESS: {address}')

    client = GoogleCivicRepresentativeClient()
    data = client.get_representatives(address=address) # officials

    for official in data:
        logger.info('Google Civic API found: {}'.format(official['name']))

    members = []
    for official in data:
        name = official['name']
        name = remove_middle_initial(name)
        try:
            member = Member.objects.get(
                Q(first_name=name['first_name']) & Q(last_name=name['last_name'])
            )
            logger.info(f'FOUND: {member}')
            members.append({
                'member_id': member.member_id,
                'first_name': member.first_name,
                'last_name': member.last_name,
                'party': member.party,
                'phone': member.phone,
                'title': member.title,
                'image': member.image,
                'office': member.office,
                'state': member.state_verbose,
                'website': member.website,
                'contact_page': member.contact_page,
                'twitter_account': member.twitter_account,
                'facebook_account': member.facebook_account,
            })
        except:
            continue
    return render(request, 'members.html', {'members': members})
