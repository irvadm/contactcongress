from django.shortcuts import render
from clients.google_civic_client import GoogleCivicClient
from django.http import HttpResponse, JsonResponse
from .forms import MemberSearchForm

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
    client = GoogleCivicClient()
    data = client.get_representatives(address=address, roles=roles)
    return JsonResponse(data, safe=False)