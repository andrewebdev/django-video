# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.views.generic import DetailView
from django.views.generic.dates import DateDetailView

from videostream.models import VideoCategory, Video
#from videostream.feeds import LatestStream

# video_info_dict = {
#     'queryset': Video.objects.filter(is_public=True),
#     'date_field': 'publish_date',
# }

# video_info_year_dict = {
#     'queryset': Video.objects.filter(is_public=True),
#     'date_field': 'publish_date',
#     'make_object_list': True,
#     'allow_empty': True,
# }

# video_info_monthday_dict = {
#     'queryset': Video.objects.filter(is_public=True),
#     'date_field': 'publish_date',
#     'allow_empty': True,
# }

urlpatterns = patterns('',

    url(r'^category/(?P<slug>[-\w]+)/$', DetailView.as_view(
            model=VideoCategory,
            context_object_name='category'
        ), name='videostream_category_detail'),


    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 
        DateDetailView.as_view(
            model=Video,
            context_object_name='video',
        ),
        name='videostream_video_detail'),

)

# feeds = {
#     'latest':  LatestStream,        
# }

# urlpatterns = patterns ('django.views.generic.date_based',
#     url(r'^$', 'archive_index', 
#         video_info_dict, 
#         name='videostream_video_archive'
#     ),
#     url(r'^(?P<year>\d{4})/$', 
#         'archive_year', 
#         video_info_year_dict,
#         name='videostream_video_year'
#     ),
#     url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$', 
#         'archive_month', 
#         video_info_monthday_dict,
#         name='videostream_video_month'
#     ),
#     url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$', 
#         'archive_day', 
#         video_info_monthday_dict,
#         name='videostream_video_day'
#     ),
#     url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 
#         'object_detail', 
#         video_info_dict,
#         name='videostream_video_detail',
#     ),
# )

# urlpatterns += patterns('django.views.generic.list_detail',
#     url(r'^id/(?P<object_id>[\d]+)/$', 'object_detail', {
#         'queryset': Video.objects.all(),
#     }, name="videostream_video_detail_id"),
# )

# urlpatterns += patterns('django.contrib.syndication.views',
#     (r'^feeds/(?P<url>.*)/$', 'feed', {'feed_dict': feeds}),
# )
