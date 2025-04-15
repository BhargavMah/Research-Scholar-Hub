from django.contrib import admin
from home.models import ResearcherProfile, Research

class ResearcherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'institution', 'department', 'research_field')
    search_fields = ['user__username', 'institution', 'research_field']

class ResearchAdmin(admin.ModelAdmin):
    list_display = ('title', 'researcher', 'category', 'efficiency_percentage', 'publication_date')
    list_filter = ('category', 'publication_date')
    search_fields = ['title', 'abstract', 'researcher__user__username']
    date_hierarchy = 'publication_date'

admin.site.register(ResearcherProfile, ResearcherProfileAdmin)
admin.site.register(Research, ResearchAdmin)
