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
            model=VideoCategory,
        ), name='videostream_category_list'),


    ## Date Based Views
    url(r'^latest/$', ArchiveIndexView.as_view(
            queryset=Video.objects.filter(is_public=True),
            date_field='publish_date',
        ), name='videostream_video_archive'),

    url(r'^(?P<year>\d{4})/(?P<month>\w+)/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', 
        DateDetailView.as_view(
            queryset=Video.objects.filter(is_public=True),
            date_field='publish_date',
        ),
        name='videostream_video_detail'),

    url(r'^(?P<year>\d{4})/(?P<month>\w+)/(?P<day>\d{1,2})/$',
        DayArchiveView.as_view(
            queryset=Video.objects.filter(is_public=True),
            date_field='publish_date',
        ), name='videostream_video_day'),

    url(r'^(?P<year>\d{4})/(?P<month>\w+)/$',
        MonthArchiveView.as_view(
            queryset=Video.objects.filter(is_public=True),
            date_field='publish_date',
        ), name='videostream_video_month'),

    url(r'^(?P<year>\d{4})/$', YearArchiveView.as_view(
            queryset=Video.objects.filter(is_public=True),
            date_field='publish_date',
        ), name='videostream_video_year'),

)

# feeds = {
#     'latest':  LatestStream,        
# }

# urlpatterns += patterns('django.contrib.syndication.views',
#     (r'^feeds/(?P<url>.*)/$', 'feed', {'feed_dict': feeds}),
# )
