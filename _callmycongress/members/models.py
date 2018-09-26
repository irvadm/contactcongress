from django.db import models
from .constants import STATES


class MemberManager(models.Manager):
    def senators(self):
        return self.filter(chamber='Senate')

    def representatives(self):
        return self.filter(chamber='House')

class Member(models.Model):
    PARTY_CHOICES = [('D', 'Democrat'), ('R', 'Republican'), ('I', 'Independent')]
    STATE_CHOICES = STATES
    CHAMBER_CHOICES = [('House', 'House'), ('Senate', 'Senate')]

    member_id = models.CharField(max_length=20, unique=True) #id
    first_name = models.CharField(max_length=60, blank=True)
    last_name = models.CharField(max_length=60, blank=True)
    district = models.CharField(max_length=12, blank=True, null=True)
    in_office = models.BooleanField()
    party = models.CharField(max_length=10, blank=True, null=True, choices=PARTY_CHOICES) #party
    state = models.CharField(max_length=2, blank=True, choices=STATE_CHOICES)
    chamber = models.CharField(max_length=8, blank=True, null=True, choices=CHAMBER_CHOICES) #data[results][0][chamber]
    office = models.CharField(max_length=200, blank=True, null=True)
    next_election = models.CharField(max_length=4, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=30, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    twitter_account = models.CharField(max_length=60, blank=True, null=True)
    facebook_account = models.CharField(max_length=60, blank=True, null=True)
    email = models.EmailField(blank=True)

    created = models.DateTimeField(auto_now_add=True) # auto_now_add: set when model is created
    updated = models.DateTimeField(auto_now=True) # auto_now: update everytime model is saved

    image = models.URLField(blank=True)

    objects = MemberManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name
    
    def clean_title(self):
        self.title = self.title.split(',')[0]
        self.save()
        return self.title


    def state_verbose(self):
        return dict(Member.STATE_CHOICES)[self.state]

    def party_verbose(self):
        return dict(Member.PARTY_CHOICES)[self.party]
