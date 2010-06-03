# -*- coding: utf-8 -*-

from django.contrib import admin

from videostream.models import *
from videostream.utils import encode_video_set

## Admin Actions
def encode_videos(modeladmin, request, queryset):
    """ Encode all selected videos """
    encode_video_set(queryset)
encode_videos.short_description = "Encode selected videos into Flash flv videos"

def mark_for_encoding(modeladmin, request, queryset):
    """ Mark selected videos for encoding """
    queryset.update(encode=True)
mark_for_encoding.short_description = "Mark videos for encoding"

def unmark_for_encoding(modeladmin, request, queryset):
    """ Unmark selected videos for encoding """
    queryset.update(encode=False)
unmark_for_encoding.short_description = "Unmark videos for encoding"

def enable_video_comments(modeladmin, request, queryset):
    """ Enable Comments on selected videos """
    queryset.update(allow_comments=True)
enable_video_comments.short_description = "Enable comments on selected videos"

def disable_video_comments(modeladmin, request, queryset):
    """ Disable comments on selected Videos """
    queryset.update(allow_comments=False)
disable_video_comments.short_description = "Disable comments on selected videos"

def publish_videos(modeladmin, request, queryset):
    """ Mark selected videos as public """
    queryset.update(is_public=True)
publish_videos.short_description = "Publish selected videos"

def unpublish_videos(modeladmin, request, queryset):
    """ Unmark selected videos as public """
    queryset.update(is_public=False)
unpublish_videos.short_description = "Unpublish selected Videos"

## ModelAdmin Classes
# We dont need the Video Model to have an Admin interface
# but I'm leaving the code commented in here just in case we
# want it sometime in the future.
#
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
    actions = [
        publish_videos, unpublish_videos,
        mark_for_encoding, unmark_for_encoding,
        enable_video_comments, disable_video_comments,
        encode_videos,
    ]

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
    actions = [publish_videos, unpublish_videos, enable_video_comments,
               disable_video_comments]

# admin.site.register(Video, VideoAdmin)
admin.site.register(VideoCategory, VideoCategoryAdmin)
admin.site.register(FlashVideo, FlashVideoAdmin)
admin.site.register(EmbedVideo, EmbedVideoAdmin)
