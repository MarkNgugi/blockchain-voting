from django.contrib import admin
from .models import *

class CandidateAdmin(admin.ModelAdmin):
    list_display = ['name', 'vote_count', 'description', 'image']
    search_fields = ['name']

admin.site.register(Candidate, CandidateAdmin)
admin.site.register(VotingTimeframe)