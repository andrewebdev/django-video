# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from django.core.management.base import NoArgsCommand
import commands
import os

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        """ Encode all pending streams
        """
        from django.conf import settings
        from videostream.models import VideoStream

        MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT')
        VIDEOSTREAM_SIZE = getattr(settings, 'VIDEOSTREAM_SIZE', '320x240')
        VIDEOSTREAM_THUMBNAIL_SIZE = getattr(settings, 'VIDEOSTREAM_THUMBNAIL_SIZE', '320x240')

        videostreams = VideoStream.objects.all().filter(encode=True)
        for stream in videostreams:
            flvfilename = "%s.flv" % stream.slug
            infile = "%s%s" % (MEDIA_ROOT, stream.videoupload)
            outfile = "%svideos/flv/%s" % (MEDIA_ROOT, flvfilename)
            thumbnailfilename = "%svideos/thumbnails/%s.png" % (MEDIA_ROOT, stream.slug)
            # ---- Final Results ----
            flvurl = "videos/flv/%s" % flvfilename
            thumburl = "videos/thumbnails/%s.png" % stream.slug
            
            # Check if flv and thumbnail folder exists and create if not
            if not(os.access("%svideos/flv/" % MEDIA_ROOT, os.F_OK)):
                os.mkdir("%svideos/flv" % MEDIA_ROOT)
            if not(os.access("%svideos/thumbnails/" % MEDIA_ROOT, os.F_OK)):
                os.mkdir("%svideos/thumbnails" % MEDIA_ROOT)

            # ffmpeg command to create flv video
            ffmpeg = "ffmpeg -y -i %s -acodec libmp3lame -ar 22050 -ab 32000 -f flv -s %s %s" % (infile, VIDEOSTREAM_SIZE, outfile)

            # ffmpeg command to create the video thumbnail
            getThumb = "ffmpeg -y -i %s -vframes 1 -ss 00:00:02 -an -vcodec png -f rawvideo -s %s %s" % (infile, VIDEOSTREAM_THUMBNAIL_SIZE, thumbnailfilename)

            # flvtool command to get the metadata
            flvtool = "flvtool2 -U %s" % outfile

            print "Input File (full path): %s " % infile
            print "Output File (full path): %s " % outfile
            print "Thumbnail Filename: %s" % thumbnailfilename
            print 80 * "-"
            print "ffmpeg Command: %s " % ffmpeg
            print "Thumbnail Command: %s " % getThumb
            print "flvTool Command: %s " % flvtool
            print 80 * "-"
            
            # Lets do the conversion
            ffmpegresult = commands.getoutput(ffmpeg)
            print "ffmpeg Result:"
            print 80 * "-"
            print ffmpegresult

            if os.access(outfile, os.F_OK): # File exists
                if (os.stat(outfile).st_size==0): # There was a error cause the outfile size is zero
                    os.remove(outfile) # We remove the file so that it does not cause confusion
                else:
                    # there does not seem to be errors, follow the rest of the procedures
                    flvtoolresult = commands.getoutput(flvtool)
                    print 80 * "-"
                    print "flvTool result: "
                    print flvtoolresult

                    thumbresult = commands.getoutput(getThumb)
                    print 80 * "-"
                    print "Thumbnail Result"
                    print thumbresult

                    stream.encode = False
                    stream.flvfile = flvurl
                    stream.thumbnail = thumburl
            stream.save()
