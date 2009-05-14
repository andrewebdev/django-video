# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from django.conf.urls.defaults import *
from videostream.models import VideoStream
from videostream.feeds import LatestStream

videostream_info_dict = {
    'queryset': VideoStream.objects.filter(is_public=True),
    'date_field': 'pub_date',
}

videostream_info_year_dict = {
    'queryset': VideoStream.objects.filter(is_public=True),
    'date_field': 'pub_date',
    'make_object_list': True,
    'allow_empty': True,
}

videostream_info_monthday_dict = {
    'queryset': VideoStream.objects.filter(is_public=True),
    'date_field': 'pub_date',
    'allow_empty': True,
}

feeds = {
    'latest':  LatestStream,        
}

urlpatterns = patterns ('django.views.generic.date_based',
    (r'^$', 'archive_index', 
                videostream_info_dict, 
                'videostream_archive_index'),
    (r'^(?P<year>\d{4})/$', 
                'archive_year', 
                videostream_info_year_dict,
                'videostream_archive_year'),
    (r'^(?P<year>\d{4})/(?P<month>\w{3})/$', 
                'archive_month', 
                videostream_info_monthday_dict,
                'videostream_archive_month'),
    (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$', 
                'archive_day', 
                videostream_info_monthday_dict,
                'videostream_archive_day'),
    (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 
                'object_detail', 
                videostream_info_dict,
                'videostream_detail'),
)

urlpatterns += patterns('django.contrib.syndication.views',
        (r'^feeds/(?P<url>.*)/$', 'feed', {'feed_dict': feeds}),
)
