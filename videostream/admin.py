from django.contrib import admin
from videostream.models import VideoStream

class VideoStreamAdmin(admin.ModelAdmin):
    prepopulated_fields = {
            'slug': ('title',),
            } 
    fieldsets = [
            ('General', {'fields': ['title', 'slug', 'description']}),
            ('Publication', {'fields': ['pub_date', 'tags', 'is_public', 'featured', 'enable_comments']}),
            ('Video Files', {'fields': ['videoupload', 'flvfile', 'thumbnail']}),
            ('Encoding Options', {'fields': ['encode']}),
            ]
    date_hierarchy = 'pub_date'
    list_display = ['title', 'flvfile', 'pub_date', 'is_public', 'featured', 'enable_comments', 'encode']
    list_filter = ['pub_date', 'is_public', 'featured','enable_comments',  'encode']
    search_fields = ['title', 'description', 'tags']

admin.site.register(VideoStream, VideoStreamAdmin)
