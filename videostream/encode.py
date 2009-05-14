#!/usr/bin/env python

import os
import commands
from optparse import OptionParser

def encodePendingStreams():
    """ Encode all pending streams
        When a stream's encode field is set to True, then this clip needs to be encoded
    """
    from django.conf import settings
    from videostream.models import VideoStream

    videostreams = VideoStream.objects.all().filter(encode=True)
    for stream in videostreams:
        flvfilename = "%s.flv" % stream.slug
        infile = "%s%s" % (settings.MEDIA_ROOT, stream.videoupload)
        outfile = "%svideos/flv/%s" % (settings.MEDIA_ROOT, flvfilename)
        thumbnailfilename = "%svideos/thumbnails/%s.png" % (settings.MEDIA_ROOT, stream.slug)
        # ---- Final Results ----
        flvurl = "videos/flv/%s" % flvfilename
        thumburl = "videos/thumbnails/%s.png" % stream.slug
        
        # Check if flv and thumbnail folder exists and create if not
        if not(os.access("%svideos/flv/" % settings.MEDIA_ROOT, os.F_OK)):
            os.mkdir("%svideos/flv" % settings.MEDIA_ROOT)
        if not(os.access("%svideos/thumbnails/" % settings.MEDIA_ROOT, os.F_OK)):
            os.mkdir("%svideos/thumbnails" % settings.MEDIA_ROOT)

        # ffmpeg command to create flv video
        ffmpeg = "ffmpeg -y -i %s -acodec libmp3lame -ar 22050 -ab 32000 -f flv -s %s %s" % (infile, settings.VIDEOSTREAM_SIZE, outfile)

        # ffmpeg command to create the video thumbnail
        getThumb = "ffmpeg -y -i %s -vframes 1 -ss 00:00:02 -an -vcodec png -f rawvideo -s %s %s" % (infile, settings.VIDEOSTREAM_THUMBNAIL_SIZE, thumbnailfilename)

        # flvtool command to get the metadata
        flvtool = "flvtool2 -U %s" % outfile

        print "Input File (full path): %s " % infile
        print "Output File (full path): %s " % outfile
        print "Thumbnail Filename: %s" % thumbnailfilename
        print "--------------"
        print "ffmpeg Command: %s " % ffmpeg
        print "Thumbnail Command: %s " % getThumb
        print "flvTool Command: %s " % flvtool
        print "--------------"
        
        # Lets do the conversion
        ffmpegresult = commands.getoutput(ffmpeg)
        print "ffmpeg Result:"
        print "--------------"
        print ffmpegresult

        if os.access(outfile, os.F_OK): # File exists
            if (os.stat(outfile).st_size==0): # There was a error cause the outfile size is zero
                os.remove(outfile) # We remove the file so that it does not cause confusion
            else:
                # there does not seem to be errors, follow the rest of the procedures
                flvtoolresult = commands.getoutput(flvtool)
                print "-------------------------"
                print "flvTool result: "
                print flvtoolresult

                thumbresult = commands.getoutput(getThumb)
                print "-------------------------"
                print "Thumbnail Result"
                print thumbresult

                stream.encode = False
                stream.flvfile = flvurl
                stream.thumbnail = thumburl
        else:
            stream.flvfilename = "Error: No Output file, please contact admin."
        stream.save()

def main():
    """ This function will first check if we are not
        already busy encoding. If so, just quit.
        If we are not encoding, call our encoding function.

        To do this, we will simply create a temporary file,
        '.encode.pid'
        Once we are finished encoding, we remove this file. If the file
        exists when the encoding script runs, then it means another
        instance of the script is already running, and we should stop.
    """
    # First check if the encoding script isn't already running
    if not os.access('.encode.pid', os.W_OK):
        # Create our temp file '.encode.pid'
        tempfile = open('.encode.pid', "w")
        tempfile.close()

        # ok, lets encode our streams
        encodePendingStreams()

        # encoding is done, lets remove the temp file
        os.remove('.encode.pid')
    else:
        print ".encode.pid exists, encoding script is already running."

if __name__ == "__main__":
    usage = "usage: %prog -s SETTINGS | --settings=SETTINGS"
    parser = OptionParser(usage)
    parser.add_option('-s', '--settings', dest='settings', metavar='SETTINGS', help="The Django Settings Module to use")
    (options, args) = parser.parse_args()
    if not options.settings:
        parser.error("You must specify a settings module")
    os.environ['DJANGO_SETTINGS_MODULE'] = options.settings
    main()
