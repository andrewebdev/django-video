# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from django.conf.urls.defaults import *
from videostream.models import *
#from videostream.feeds import LatestStream

video_info_dict = {
    'queryset': Video.objects.filter(is_public=True),
    'date_field': 'publish_date',
}

video_info_year_dict = {
    'queryset': Video.objects.filter(is_public=True),
    'date_field': 'publish_date',
    'make_object_list': True,
    'allow_empty': True,
}

video_info_monthday_dict = {
    'queryset': Video.objects.filter(is_public=True),
    'date_field': 'publish_date',
    'allow_empty': True,
}

# feeds = {
#     'latest':  LatestStream,        
# }

urlpatterns = patterns ('django.views.generic.date_based',
    url(r'^$', 'archive_index', 
        video_info_dict, 
        name='videostream_video_archive'
    ),
    url(r'^(?P<year>\d{4})/$', 
        'archive_year', 
        video_info_year_dict,
        name='videostream_video_year'
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$', 
        'archive_month', 
        video_info_monthday_dict,
        name='videostream_video_month'
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$', 
        'archive_day', 
        video_info_monthday_dict,
        name='videostream_video_day'
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 
        'object_detail', 
        video_info_dict,
        name='videostream_video_detail'
    ),
)

# urlpatterns += patterns('django.contrib.syndication.views',
#     (r'^feeds/(?P<url>.*)/$', 'feed', {'feed_dict': feeds}),
# )
