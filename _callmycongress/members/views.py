from django.shortcuts import render
from clients.clients import GoogleCivicRepresentativeClient
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from .forms import MemberSearchForm
from .models import Member
import logging

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'index.html')

def search(request):
    address = request.GET.get('address', '')
    if request.GET.get('roles') == '':
        roles = ['legislatorUpperBody', 'legislatorLowerBody']
    else:
        roles = request.GET.get('roles')
    print('REQUEST.GET')
    print(request.GET)
    
    print('address: {}'.format(address))
    print('roles: {}'.format(roles))

    client = GoogleCivicRepresentativeClient()
    data = client.get_representatives(address=address, roles=roles) # officials
    members = []
    for official in data:
        name = official['name']
        name = name.split() #['Mark', 'R.', 'Warner']
        first_name = name[0]
        last_name = name[len(name) - 1]
        try:
            member = Member.objects.get(
                Q(first_name=first_name) & Q(last_name=last_name)
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
                'state': member.state,
                'website': member.website,
            })
        except:
            continue
    logger.info(members)
    return JsonResponse(members, safe=False)