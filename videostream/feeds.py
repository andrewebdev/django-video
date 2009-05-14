from django.contrib.syndication.feeds import Feed
from django.conf import settings

from videostream.models import VideoStream

class LatestStream(Feed):
    title = settings.VIDEOSTREAM_FEED_TITLE
    description = settings.VIDEOSTREAM_FEED_DESCRIPTION
    link = settings.VIDEOSTREAM_FEED_LINK

    def items(self):
        return VideoStream.objects.all().filter(is_public=True)[:5]
