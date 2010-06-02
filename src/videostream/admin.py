# -*- coding: utf-8 -*-

from django.contrib import admin
from videostream.models import *

# class VideoAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('title',)} 
#     date_hierarchy = 'publish_date'
#     list_display = [
#         'title', 'slug', 'publish_date', 'is_public',
#         'allow_comments',
#     ]
#     list_filter = [
#         'created_date', 'publish_date', 'modified_date',
#         'is_public', 'allow_comments',
#     ]
#     search_fields = ['title', 'description', 'tags']

class VideoCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'slug']

class FlashVideoAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'slug', 'publish_date', 'is_public',
        'allow_comments', 'encode',
    ]
    list_filter = [
        'created_date', 'publish_date', 'modified_date',
        'is_public', 'allow_comments', 'encode',
    ]
    prepopulated_fields = {'slug': ('title',)} 
    fieldsets = (
        ('Video Details', {'fields': [
            'title', 'slug', 'description', 'tags', 'is_public',
            'allow_comments', 'publish_date', 'categories',
        ]}),

        ('Video Source', {'fields': [
            'videoupload', 'flvfile', 'thumbnail', 'encode'
        ]})
    )
    date_hierarchy = 'publish_date'
    search_fields = ['title', 'description', 'tags']

class EmbedVideoAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'slug', 'publish_date', 'is_public',
        'allow_comments', 'video_url',
    ]
    list_filter = [
        'created_date', 'publish_date', 'modified_date',
        'is_public', 'allow_comments',
    ]
    prepopulated_fields = {'slug': ('title',)} 
    fieldsets = (
        ('Video Details', {'fields': [
            'title', 'slug', 'description', 'tags', 'is_public',
            'allow_comments', 'publish_date', 'categories',
        ]}),

        ('Video Source', {'fields': [
            'video_url', 'video_code',
        ]})
    )
    date_hierarchy = 'publish_date'
    search_fields = ['title', 'description', 'tags']

# admin.site.register(Video, VideoAdmin)
admin.site.register(VideoCategory, VideoCategoryAdmin)
admin.site.register(FlashVideo, FlashVideoAdmin)
admin.site.register(EmbedVideo, EmbedVideoAdmin)
