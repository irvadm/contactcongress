from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    model = Member
    list_display = ['member_id', 'first_name', 'last_name', 'chamber', 'image', 'district', 'state', 'updated']
    list_editable = ['image']
    list_filter = ['chamber', 'state', 'party', 'in_office']
    search_fields = ['member_id', 'first_name', 'last_name',]
