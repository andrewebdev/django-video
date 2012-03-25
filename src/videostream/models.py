# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# use Django-tagging for tags. If Django-tagging cannot be found, create our own
# I did not author this little snippet, I found it somewhere on the web,
# and cannot remember where exactly it was.
try:
    from tagging.fields import TagField
    tagfield_help_text = 'Separate tags with spaces, put quotes around multiple-word tags.'
except ImportError:
    class TagField(models.CharField):
        def __init__(self, **kwargs):
            default_kwargs = {'max_length': 255, 'blank': True}
            default_kwargs.update(kwargs)
            super(TagField, self).__init__(**default_kwargs)
        def get_internal_type(self):
            return 'CharField'
    tagfield_help_text = 'Django-tagging was not found, tags will be treated as plain text.'
# End tagging snippet


class VideoCategory(models.Model):
    """ A model to help categorize videos """
    title = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True,
        help_text="A url friendly slug for the category",
    )
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Video Categories"

    def __unicode__(self):
        return "%s" % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('videostream_category_detail', [self.slug])


class Video(models.Model):
    """
    This is our Base Video Class, with fields that will be available
    to all other Video models.
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,
        help_text="A url friendly slug for the video clip.")
    description = models.TextField(null=True, blank=True)

    tags = TagField(help_text=tagfield_help_text)
    categories = models.ManyToManyField(VideoCategory)
    allow_comments = models.BooleanField(default=False)

    ## TODO:
    ## In future we may want to allow for more control over publication
    is_public = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(null=True, blank=True)

    author = models.ForeignKey(User, null=True, blank=True)
    
    class Meta:
        ordering = ('-publish_date', '-created_date')
        get_latest_by = 'publish_date'

    def __unicode__(self):
        return "%s" % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('videostream_video_detail', (), { 
            'year': self.publish_date.strftime("%Y"),
            'month': self.publish_date.strftime("%b"),
            'day': self.publish_date.strftime("%d"), 
            'slug': self.slug 
        })

    def save(self, *args, **kwargs):
        self.modified_date = datetime.now()
        if self.publish_date == None and self.is_public:
            self.publish_date = datetime.now()
        super(Video, self).save(*args, **kwargs)


class BasicVideo(Video):
    """
    This is our basic HTML5 Video type. BasicVideo can have more than
    one HTML5 Video as a 'video type'. This allows us to create different
    video formats, one for each type format.
    """
    pass


class HTML5Video(models.Model):
    OGG = 0
    WEBM = 1
    MP4 = 2
    FLASH = 3
    VIDEO_TYPE = (
        (OGG, 'video/ogg'),
        (WEBM, 'video/webm'),
        (MP4, 'video/mp4'),
        (FLASH, 'video/flv'),
    )

    video_type = models.IntegerField(
        choices=VIDEO_TYPE,
        default=WEBM,
        help_text="The Video type"
    )
    video_file = models.FileField(
        upload_to="videos/html5/",
        help_text="The file you wish to upload. Make sure that it's the correct format.",
    )

    # Allow for multiple video types for a single video
    basic_video = models.ForeignKey(BasicVideo)

    class Meta:
        verbose_name = "Html 5 Video"
        verbose_name_plural = "Html 5 Videos"


class EmbedVideo(Video):
    video_url = models.URLField(null=True, blank=True)
    video_code = models.TextField(
        null=True,
        blank=True,
        help_text="Use the video embed code instead of the url if your frontend does not support embedding with the URL only."
    )


class FlashVideo(Video):
    """
    This model is what was once called "VideoStream". Since we want to support
    videos from other sources as well, this model was renamed to FlashVideo.
    """
    original_file = models.FileField(
        upload_to="videos/flash/source/",
        null=True,
        blank=True,
        help_text="Make sure that the video you are uploading has a audo bitrate of at least 16. The encoding wont function on a lower audio bitrate."
    )

    flv_file = models.FileField(
        upload_to="videos/flash/flv/",
        null=True,
        blank=True,
        help_text="If you already have an encoded flash video, upload it here (no encoding needed)."
    )

    thumbnail = models.ImageField(
        blank=True,
        null=True, 
        upload_to="videos/flash/thumbnails/",
        help_text="If you uploaded a flv clip that was already encoded, you will need to upload a thumbnail as well. If you are planning use django-video to encode, you dont have to upload a thumbnail, as django-video will create it for you"
    )

    # This option allows us to specify whether we need to encode the clip
    encode = models.BooleanField(
        default=False,
        help_text="Encode or Re-Encode the clip. If you only wanted to change some information on the item, and do not want to encode the clip again, make sure this option is not selected."
    )

    def get_player_size(self):
        """ this method returns the styles for the player size """
        size = getattr(settings, 'VIDEOSTREAM_SIZE', '320x240').split('x')
        return "width: %spx; height: %spx;" % (size[0], size[1])
