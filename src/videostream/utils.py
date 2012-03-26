# -*- coding: utf-8 -*-

import commands
import os

from django.conf import settings

from videostream.models import FlashVideo


# This allows the developer to override the binary path for ffmpeg
FFMPEG_BINARY_PATH = getattr(settings, 'FFMPEG_BINARY_PATH', 'ffmpeg')
FLVTOOL_PATH = getattr(settings, 'FLVTOOL_PATH', 'flvtool2')


def encode_video(flashvideo):
    """
    Encode a single Video where ``flashvideo`` is an instance of
    videostream.models.FlashVideo
    """
    MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT')
    VIDEOSTREAM_SIZE = getattr(settings, 'VIDEOSTREAM_SIZE', '320x240')
    VIDEOSTREAM_THUMBNAIL_SIZE = getattr(settings,
        'VIDEOSTREAM_THUMBNAIL_SIZE', '320x240')

    flvfilename = "%s.flv" % flashvideo.slug
    infile = "%s/%s" % (MEDIA_ROOT, flashvideo.original_file)
    outfile = "%s/videos/flash/flv/%s" % (MEDIA_ROOT, flvfilename)
    thumbnailfilename = "%s/videos/flash/thumbnails/%s.png" % (
        MEDIA_ROOT, flashvideo.slug)

    # Final Results
    flvurl = "videos/flash/flv/%s" % flvfilename
    thumburl = "videos/flash/thumbnails/%s.png" % flashvideo.slug

    # Check if flv and thumbnail folder exists and create if not
    if not(os.access("%s/videos/flash/flv/" % MEDIA_ROOT, os.F_OK)):
        os.makedirs("%s/videos/flash/flv" % MEDIA_ROOT)

    if not(os.access("%s/videos/flash/thumbnails/" % MEDIA_ROOT, os.F_OK)):
        os.makedirs("%s/videos/flash/thumbnails" % MEDIA_ROOT)

    # ffmpeg command to create flv video
    ffmpeg = "%s -y -i %s -acodec libmp3lame -ar 22050 -ab 32000 -f flv -s %s %s" % (
        FFMPEG_BINARY_PATH, infile, VIDEOSTREAM_SIZE, outfile)

    # ffmpeg command to create the video thumbnail
    getThumb = "%s -y -i %s -vframes 1 -ss 00:00:02 -an -vcodec png -f rawvideo -s %s %s" % (
        FFMPEG_BINARY_PATH, infile, VIDEOSTREAM_THUMBNAIL_SIZE, thumbnailfilename)

    # flvtool command to get the metadata
    flvtool = "%s -U %s" % (FLVTOOL_PATH, outfile)

    # Lets do the conversion
    ffmpegresult = commands.getoutput(ffmpeg)
    print 80*"~"
    print ffmpegresult

    if os.access(outfile, os.F_OK): # outfile exists

        # There was a error cause the outfile size is zero
        if (os.stat(outfile).st_size==0): 
            # We remove the file so that it does not cause confusion
            os.remove(outfile)

        else:
            # there does not seem to be errors, follow the rest of the procedures
            flvtoolresult = commands.getoutput(flvtool)
            print flvtoolresult

            thumbresult = commands.getoutput(getThumb)
            print thumbresult

            flashvideo.encode = False
            flashvideo.flv_file = flvurl
            flashvideo.thumbnail = thumburl

    print 80*"~"
    flashvideo.save()


def encode_video_set(queryset=None):

    if not queryset:
        queryset = FlashVideo.objects.filter(encode=True)

    for flashvideo in queryset:
        encode_video(flashvideo)

