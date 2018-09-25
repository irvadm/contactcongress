from django.shortcuts import render
from clients.clients import GoogleCivicRepresentativeClient
from django.http import HttpResponse, JsonResponse
from .forms import MemberSearchForm
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
    for official in data:
        print(official)


    return JsonResponse(data, safe=False)