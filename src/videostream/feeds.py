# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from django.contrib.syndication.feeds import Feed
from django.conf import settings
from videostream.models import VideoStream

class LatestStream(Feed):
    title = getattr(settings, 'VIDEOSTREAM_FEED_TITLE', 'Video Feeds')
    description = getattr(settings, 'VIDEOSTREAM_FEED_DESCRIPTION', 'Video Feeds')
    link = getattr(settings, 'VIDEOSTREAM_FEED_LINK', '')

    def items(self):
        return VideoStream.objects.all().filter(is_public=True)[:5]
