# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from django.views.generic.dates import *

from videostream.models import VideoCategory, Video
#from videostream.feeds import LatestStream


urlpatterns = patterns('',

    url(r'^category/(?P<slug>[-\w]+)/$', DetailView.as_view(
            model=VideoCategory, context_object_name='category'
        ), name='videostream_category_detail'),

    url(r'^categories/$', ListView.as_view(
            model=VideoCategory, context_object_name='category_list'
        ), name='videostream_category_list'),


    url(r'^$', ArchiveIndexView.as_view(
            queryset=Video.objects.filter(is_public=True),
            context_object_name='video_list',
        ), name='videostream_video_archive'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 
        DateDetailView.as_view(
            queryset=Video.objects.filter(is_public=True),
            context_object_name='video',
        ),
        name='videostream_video_detail'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        DayArchiveView.as_view(
            queryset=Video.objects.filter(is_public=True),
            context_object_name='video_list',
        ), name='videostream_video_day'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        MonthArchiveView.as_view(
            queryset=Video.objects.filter(is_public=True),
            context_object_name='video_list',
        ), name='videostream_video_month'),

    url(r'^(?P<year>\d{4})/$', YearArchiveView.as_view(
            queryset=Video.objects.filter(is_public=True),
            context_object_name='video_list',
        ), name='videostream_video_year'),

)

# feeds = {
#     'latest':  LatestStream,        
# }

# urlpatterns += patterns('django.contrib.syndication.views',
#     (r'^feeds/(?P<url>.*)/$', 'feed', {'feed_dict': feeds}),
# )
